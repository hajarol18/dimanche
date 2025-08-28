/** @odoo-module **/

import { registry } from '@web/core/registry';
import { useRef, onMounted, onWillUnmount } from '@odoo/owl';

/**
 * Widget Leaflet pour afficher les parcelles sur une carte
 */
export class LeafletMapRenderer extends owl.Component {
    setup() {
        this.mapRef = useRef('map');
        this.map = null;
        this.markers = [];
        this.polygons = [];
        this.currentParcelleId = null;
        
        onMounted(() => this.initMap());
        onWillUnmount(() => this.destroyMap());
    }
    
    /**
     * Initialise la carte Leaflet
     */
    initMap() {
        if (!this.mapRef.el) return;
        
        try {
            // Création de la carte
            this.map = L.map(this.mapRef.el).setView([46.603354, 1.888334], 6); // Centre sur la France
            
            // Ajout du fond de carte OpenStreetMap
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19
            }).addTo(this.map);
            
            // Chargement des données
            this.loadMapData();
            
            // Gestion des événements de clic sur la carte
            this.map.on('click', () => this.clearSelection());
            
        } catch (error) {
            console.error('Erreur lors de l\'initialisation de la carte Leaflet:', error);
        }
    }
    
    /**
     * Charge les données des parcelles pour les afficher sur la carte
     */
    async loadMapData() {
        if (!this.map) return;
        
        try {
            // Récupération des données depuis le modèle
            const data = await this.env.services.rpc({
                model: 'smart_agri_parcelle',
                method: 'get_map_data',
                args: [],
                kwargs: {}
            });
            
            // Nettoyage des marqueurs et polygones existants
            this.clearMapLayers();
            
            // Ajout des parcelles à la carte
            if (data && data.length > 0) {
                const bounds = L.latLngBounds();
                
                data.forEach(parcelle => {
                    this.addParcelleToMap(parcelle, bounds);
                });
                
                // Ajustement de la vue pour montrer toutes les parcelles
                if (bounds.isValid()) {
                    this.map.fitBounds(bounds, { padding: [20, 20] });
                }
            }
        } catch (error) {
            console.error('Erreur lors du chargement des données de la carte:', error);
        }
    }
    
    /**
     * Ajoute une parcelle à la carte
     * @param {Object} parcelle - Données de la parcelle
     * @param {L.LatLngBounds} bounds - Limites pour ajuster la vue
     */
    addParcelleToMap(parcelle, bounds) {
        if (!parcelle) return;
        
        try {
            let layer;
            
            // Si la parcelle a un polygone
            if (parcelle.has_polygon && parcelle.geo_polygon) {
                layer = L.geoJSON(parcelle.geo_polygon, {
                    style: {
                        fillColor: '#3388ff',
                        weight: 2,
                        opacity: 1,
                        color: '#3388ff',
                        fillOpacity: 0.4
                    }
                }).addTo(this.map);
                
                // Ajout aux limites
                bounds.extend(layer.getBounds());
                
                // Sauvegarde pour nettoyage ultérieur
                this.polygons.push(layer);
                
            } else if (parcelle.latitude && parcelle.longitude) {
                // Si la parcelle n'a qu'un point
                const icon = L.divIcon({
                    className: 'parcelle-marker',
                    html: `<div class="marker-content">${parcelle.code}</div>`,
                    iconSize: [30, 30],
                    iconAnchor: [15, 15]
                });
                
                layer = L.marker([parcelle.latitude, parcelle.longitude], { icon: icon })
                    .addTo(this.map);
                
                // Ajout aux limites
                bounds.extend([parcelle.latitude, parcelle.longitude]);
                
                // Sauvegarde pour nettoyage ultérieur
                this.markers.push(layer);
            }
            
            // Ajout du popup avec les informations de la parcelle
            if (layer) {
                layer.bindPopup(this.createParcellePopup(parcelle));
                
                // Gestion du clic sur la parcelle
                layer.on('click', () => this.selectParcelle(parcelle.id, layer));
            }
            
        } catch (error) {
            console.error('Erreur lors de l\'ajout de la parcelle à la carte:', error);
        }
    }
    
    /**
     * Crée un popup pour afficher les informations d'une parcelle
     * @param {Object} parcelle - Données de la parcelle
     * @returns {string} HTML du popup
     */
    createParcellePopup(parcelle) {
        const html = `
            <div class="parcelle-popup">
                <h4>${parcelle.name}</h4>
                <p><strong>Code:</strong> ${parcelle.code}</p>
                <p><strong>Surface:</strong> ${parcelle.surface} ha</p>
                ${parcelle.exploitation ? `<p><strong>Exploitation:</strong> ${parcelle.exploitation}</p>` : ''}
                ${parcelle.type_sol ? `<p><strong>Type de sol:</strong> ${parcelle.type_sol}</p>` : ''}
                ${parcelle.irrigation ? '<p><strong>✓ Irrigation disponible</strong></p>' : ''}
                ${parcelle.drainage ? '<p><strong>✓ Drainage disponible</strong></p>' : ''}
                <div class="popup-actions">
                    <button class="btn btn-primary btn-sm" onclick="window.location.href='/web#id=${parcelle.id}&model=smart_agri_parcelle&view_type=form'">
                        Voir détails
                    </button>
                </div>
            </div>
        `;
        return html;
    }
    
    /**
     * Sélectionne une parcelle sur la carte
     * @param {number} parcelleId - ID de la parcelle
     * @param {L.Layer} layer - Couche Leaflet de la parcelle
     */
    selectParcelle(parcelleId, layer) {
        // Désélection de la parcelle précédente
        this.clearSelection();
        
        // Sélection de la nouvelle parcelle
        this.currentParcelleId = parcelleId;
        
        // Mise en évidence de la parcelle sélectionnée
        if (layer instanceof L.GeoJSON) {
            layer.setStyle({
                fillColor: '#ff6b35',
                weight: 3,
                color: '#ff6b35',
                fillOpacity: 0.6
            });
        } else if (layer instanceof L.Marker) {
            layer.getElement().classList.add('selected');
        }
        
        // Centrage de la carte sur la parcelle
        if (layer.getBounds) {
            this.map.fitBounds(layer.getBounds(), { padding: [50, 50] });
        } else {
            this.map.setView(layer.getLatLng(), Math.max(this.map.getZoom(), 12));
        }
    }
    
    /**
     * Efface la sélection actuelle
     */
    clearSelection() {
        if (this.currentParcelleId) {
            // Restauration du style normal pour toutes les parcelles
            this.polygons.forEach(polygon => {
                polygon.setStyle({
                    fillColor: '#3388ff',
                    weight: 2,
                    color: '#3388ff',
                    fillOpacity: 0.4
                });
            });
            
            this.markers.forEach(marker => {
                marker.getElement()?.classList.remove('selected');
            });
            
            this.currentParcelleId = null;
        }
    }
    
    /**
     * Nettoie les couches de la carte
     */
    clearMapLayers() {
        // Suppression des polygones
        this.polygons.forEach(polygon => {
            if (this.map && this.map.hasLayer(polygon)) {
                this.map.removeLayer(polygon);
            }
        });
        this.polygons = [];
        
        // Suppression des marqueurs
        this.markers.forEach(marker => {
            if (this.map && this.map.hasLayer(marker)) {
                this.map.removeLayer(marker);
            }
        });
        this.markers = [];
        
        // Effacement de la sélection
        this.clearSelection();
    }
    
    /**
     * Détruit la carte
     */
    destroyMap() {
        if (this.map) {
            this.clearMapLayers();
            this.map.remove();
            this.map = null;
        }
    }
    
    /**
     * Rafraîchit la carte
     */
    refreshMap() {
        this.loadMapData();
    }
}

// Enregistrement du composant
registry.category('components').add('LeafletMapRenderer', LeafletMapRenderer);

// Template pour le composant
LeafletMapRenderer.template = 'smart_agri_decision.LeafletMapTemplate';