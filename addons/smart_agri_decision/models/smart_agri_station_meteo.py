# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class SmartAgriStationMeteo(models.Model):
    """Gestion des stations météo avec logique métier claire"""
    
    _name = 'smart_agri_station_meteo'
    _description = 'Station Météo - Gestion Centralisée'
    _order = 'name'
    
    # ========================================
    # CHAMPS D'IDENTIFICATION
    # ========================================
    name = fields.Char('Nom de la station', required=True)
    code = fields.Char('Code unique', required=True, copy=False)
    description = fields.Text('Description de la station')
    
    # ========================================
    # GÉOLOCALISATION
    # ========================================
    latitude = fields.Float('Latitude', required=True, digits=(10, 6))
    longitude = fields.Float('Longitude', required=True, digits=(10, 6))
    altitude = fields.Float('Altitude (m)', digits=(6, 1))
    precision_geolocalisation = fields.Float('Précision géolocalisation (m)', default=100.0)
    
    # ========================================
    # TYPE ET SOURCE DE DONNÉES
    # ========================================
    type_station = fields.Selection([
        ('meteostat', '📡 Station Meteostat'),
        ('meteo_france', '🇫🇷 Météo France'),
        ('station_locale', '🏠 Station Locale'),
        ('api_externe', '🔗 API Externe'),
        ('satellite', '🛰️ Données Satellite'),
        ('autre', '⚙️ Autre')
    ], string='Type de station', required=True, default='meteostat')
    
    source_donnees = fields.Char('Source des données', required=True)
    url_api = fields.Char('URL de l\'API')
    cle_api = fields.Char('Clé API', help='Clé d\'accès à l\'API')
    
    # ======================================== 
    # PARAMÈTRES MÉTÉOROLOGIQUES DISPONIBLES
    # ========================================
    parametres_disponibles = fields.Many2many('smart_agri_parametre_meteo', string='Paramètres disponibles')
    
    # ========================================
    # FRÉQUENCE ET QUALITÉ DES DONNÉES
    # ========================================
    frequence_mise_a_jour = fields.Selection([
        ('temps_reel', '⏰ Temps réel (5-15 min)'),
        ('horaire', '🕐 Horaire'),
        ('quotidien', '📅 Quotidien'),
        ('hebdomadaire', '📅 Hebdomadaire'),
        ('mensuel', '📅 Mensuel')
    ], string='Fréquence de mise à jour', required=True, default='quotidien')
    
    qualite_donnees = fields.Selection([
        ('excellente', '⭐ Excellente (>95%)'),
        ('bonne', '⭐⭐ Bonne (85-95%)'),
        ('moyenne', '⭐⭐⭐ Moyenne (70-85%)'),
        ('faible', '⭐⭐⭐⭐ Faible (<70%)')
    ], string='Qualité des données', default='bonne')
    
    # ========================================
    # STATUT ET ACTIVITÉ
    # ========================================
    state = fields.Selection([
        ('active', '✅ Active'),
        ('inactive', '❌ Inactive'),
        ('maintenance', '🔧 En maintenance'),
        ('erreur', '🚨 Erreur'),
        ('test', '🧪 En test')
    ], string='Statut', default='active')
    
    date_activation = fields.Date('Date d\'activation')
    date_derniere_donnee = fields.Datetime('Dernière donnée reçue')
    date_maintenance = fields.Date('Dernière maintenance')
    
    # ========================================
    # RELATIONS AVEC LES EXPLOITATIONS
    # ========================================
    exploitations_associees = fields.Many2many('smart_agri_exploitation', string='Exploitations associées')
    rayon_couverture = fields.Float('Rayon de couverture (km)', default=50.0, help='Rayon dans lequel cette station peut fournir des données fiables')
    
    # ========================================
    # CONFIGURATION TECHNIQUE
    # ========================================
    format_donnees = fields.Selection([
        ('json', 'JSON'),
        ('xml', 'XML'),
        ('csv', 'CSV'),
        ('autre', 'Autre')
    ], string='Format des données', default='json')
    
    encodage = fields.Char('Encodage', default='UTF-8')
    fuseau_horaire = fields.Selection([
        ('UTC', 'UTC'),
        ('Europe/Paris', 'Europe/Paris'),
        ('Europe/Brussels', 'Europe/Brussels'),
        ('autre', 'Autre')
    ], string='Fuseau horaire', default='Europe/Paris')
    
    # ========================================
    # MÉTRIQUES DE PERFORMANCE
    # ========================================
    taux_disponibilite = fields.Float('Taux de disponibilité (%)', default=99.0)
    taux_erreur = fields.Float('Taux d\'erreur (%)', default=1.0)
    temps_reponse_moyen = fields.Float('Temps de réponse moyen (ms)', default=500.0)
    
    # ========================================
    # NOTES ET DOCUMENTATION
    # ========================================
    notes = fields.Text('Notes techniques')
    documentation_url = fields.Char('URL de la documentation')
    contact_technique = fields.Char('Contact technique')
    
    # ========================================
    # CHAMPS COMPUTÉS
    # ========================================
    nombre_exploitations = fields.Integer('Nombre d\'exploitations', compute='_compute_nombre_exploitations', store=True)
    distance_exploitation_proche = fields.Float('Distance exploitation la plus proche (km)', compute='_compute_distance_exploitation')
    statut_operational = fields.Selection([
        ('operationnel', '🟢 Opérationnel'),
        ('attention', '🟡 Attention'),
        ('probleme', '🟠 Problème'),
        ('critique', '🔴 Critique')
    ], string='Statut opérationnel', compute='_compute_statut_operational', store=True)
    
    # ========================================
    # MÉTHODES COMPUTÉES
    # ========================================
    
    @api.depends('exploitations_associees')
    def _compute_nombre_exploitations(self):
        """Calcule le nombre d'exploitations associées"""
        for record in self:
            record.nombre_exploitations = len(record.exploitations_associees)
    
    @api.depends('exploitations_associees', 'latitude', 'longitude')
    def _compute_distance_exploitation(self):
        """Calcule la distance à l'exploitation la plus proche"""
        for record in self:
            if record.exploitations_associees:
                distances = []
                for exploitation in record.exploitations_associees:
                    if exploitation.latitude and exploitation.longitude:
                        # Calcul simple de distance (formule de Haversine simplifiée)
                        import math
                        lat1, lon1 = math.radians(record.latitude), math.radians(record.longitude)
                        lat2, lon2 = math.radians(exploitation.latitude), math.radians(exploitation.longitude)
                        
                        dlat = lat2 - lat1
                        dlon = lon2 - lon1
                        
                        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
                        c = 2 * math.asin(math.sqrt(a))
                        distance = 6371 * c  # Rayon de la Terre en km
                        
                        distances.append(distance)
                
                if distances:
                    record.distance_exploitation_proche = min(distances)
                else:
                    record.distance_exploitation_proche = 0.0
            else:
                record.distance_exploitation_proche = 0.0
    
    @api.depends('state', 'taux_disponibilite', 'taux_erreur', 'date_derniere_donnee')
    def _compute_statut_operational(self):
        """Calcule le statut opérationnel de la station"""
        for record in self:
            if record.state != 'active':
                record.statut_operational = 'probleme'
            elif record.taux_disponibilite < 90:
                record.statut_operational = 'critique'
            elif record.taux_erreur > 5:
                record.statut_operational = 'attention'
            elif record.date_derniere_donnee:
                # Vérifier si les données sont récentes
                delai = datetime.now() - record.date_derniere_donnee
                if delai.days > 7:
                    record.statut_operational = 'attention'
                else:
                    record.statut_operational = 'operationnel'
            else:
                record.statut_operational = 'attention'
    
    # ========================================
    # MÉTHODES MÉTIER
    # ========================================
    
    def action_activer_station(self):
        """Active la station météo"""
        for record in self:
            record.state = 'active'
            record.date_activation = fields.Date.today()
            record._compute_statut_operational()
    
    def action_desactiver_station(self):
        """Désactive la station météo"""
        for record in self:
            record.state = 'inactive'
            record._compute_statut_operational()
    
    def action_maintenance(self):
        """Met la station en maintenance"""
        for record in self:
            record.state = 'maintenance'
            record.date_maintenance = fields.Date.today()
            record._compute_statut_operational()
    
    def action_tester_connexion(self):
        """Teste la connexion à la station"""
        for record in self:
            try:
                # Simulation de test de connexion
                _logger.info(f"Test de connexion à la station {record.name}")
                # Ici, on pourrait implémenter un vrai test d'API
                record.message_post(body="✅ Test de connexion réussi")
            except Exception as e:
                record.message_post(body=f"❌ Erreur de connexion: {str(e)}")
    
    def action_importer_donnees_test(self):
        """Importe des données de test pour valider la station"""
        for record in self:
            try:
                # Création de données de test
                self.env['smart_agri_meteo'].create({
                    'name': f'Test - {record.name}',
                    'exploitation_id': record.exploitations_associees[0].id if record.exploitations_associees else False,
                    'date_mesure': fields.Date.today(),
                    'temperature': 20.0,
                    'humidite': 65.0,
                    'precipitation': 0.0,
                    'source_station': record.id,
                    'notes': 'Données de test pour validation de la station'
                })
                record.message_post(body="✅ Données de test importées avec succès")
            except Exception as e:
                record.message_post(body=f"❌ Erreur lors de l'import des données de test: {str(e)}")
    
    # ========================================
    # VALIDATIONS
    # ========================================
    
    @api.constrains('latitude', 'longitude')
    def _check_coordinates(self):
        """Vérifie la validité des coordonnées"""
        for record in self:
            if record.latitude < -90 or record.latitude > 90:
                raise ValidationError(_('La latitude doit être comprise entre -90 et 90 degrés.'))
            if record.longitude < -180 or record.longitude > 180:
                raise ValidationError(_('La longitude doit être comprise entre -180 et 180 degrés.'))
    
    @api.constrains('rayon_couverture')
    def _check_rayon_couverture(self):
        """Vérifie le rayon de couverture"""
        for record in self:
            if record.rayon_couverture <= 0:
                raise ValidationError(_('Le rayon de couverture doit être strictement positif.'))
            if record.rayon_couverture > 1000:
                raise ValidationError(_('Le rayon de couverture ne peut pas dépasser 1000 km.'))
    
    @api.constrains('taux_disponibilite', 'taux_erreur')
    def _check_metriques(self):
        """Vérifie les métriques de performance"""
        for record in self:
            if record.taux_disponibilite < 0 or record.taux_disponibilite > 100:
                raise ValidationError(_('Le taux de disponibilité doit être compris entre 0 et 100%.'))
            if record.taux_erreur < 0 or record.taux_erreur > 100:
                raise ValidationError(_('Le taux d\'erreur doit être compris entre 0 et 100%.'))
    
    # ========================================
    # MÉTHODES DE RECHERCHE
    # ========================================
    
    @api.model
    def rechercher_station_proche(self, latitude, longitude, rayon_max=100):
        """Recherche la station météo la plus proche d'un point donné"""
        stations = self.search([
            ('state', '=', 'active'),
            ('statut_operational', '=', 'operationnel')
        ])
        
        station_proche = False
        distance_min = float('inf')
        
        for station in stations:
            # Calcul de distance (formule de Haversine simplifiée)
            import math
            lat1, lon1 = math.radians(latitude), math.radians(longitude)
            lat2, lon2 = math.radians(station.latitude), math.radians(station.longitude)
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            distance = 6371 * c  # Rayon de la Terre en km
            
            if distance <= rayon_max and distance < distance_min:
                distance_min = distance
                station_proche = station
        
        return station_proche, distance_min
    
    # ========================================
    # MÉTHODES D'INITIALISATION
    # ========================================
    
    @api.model
    def creer_station_meteostat(self, nom, latitude, longitude, exploitation_id=False):
        """Crée automatiquement une station Meteostat pour une exploitation"""
        station = self.create({
            'name': nom,
            'code': f'METEO_{nom.upper().replace(" ", "_")}',
            'type_station': 'meteostat',
            'source_donnees': 'Meteostat API',
            'latitude': latitude,
            'longitude': longitude,
            'frequence_mise_a_jour': 'quotidien',
            'rayon_couverture': 50.0,
            'state': 'active'
        })
        
        if exploitation_id:
            station.exploitations_associees = [(4, exploitation_id)]
        
        return station


class SmartAgriParametreMeteo(models.Model):
    """Paramètres météorologiques disponibles"""
    
    _name = 'smart_agri_parametre_meteo'
    _description = 'Paramètre Météorologique'
    _order = 'name'
    
    name = fields.Char('Nom du paramètre', required=True)
    code = fields.Char('Code', required=True)
    unite = fields.Char('Unité de mesure', required=True)
    description = fields.Text('Description')
    icone = fields.Char('Icône', default='🌡️')
    
    # Catégorie du paramètre
    categorie = fields.Selection([
        ('temperature', '🌡️ Température'),
        ('humidite', '💧 Humidité'),
        ('precipitation', '🌧️ Précipitations'),
        ('vent', '💨 Vent'),
        ('pression', '🌪️ Pression'),
        ('ensoleillement', '☀️ Ensoleillement'),
        ('autre', '⚙️ Autre')
    ], string='Catégorie', required=True)
    
    # Paramètres de validation
    valeur_min = fields.Float('Valeur minimale')
    valeur_max = fields.Float('Valeur maximale')
    valeur_defaut = fields.Float('Valeur par défaut')
    
    # Importance pour l'agriculture
    importance_agricole = fields.Selection([
        ('critique', '🔴 Critique'),
        ('elevee', '🟠 Élevée'),
        ('moyenne', '🟡 Moyenne'),
        ('faible', '🟢 Faible')
    ], string='Importance agricole', default='moyenne')
    
    active = fields.Boolean('Actif', default=True)
    
    @api.model
    def initialiser_parametres_standards(self):
        """Initialise les paramètres météorologiques standards"""
        parametres = [
            # Températures
            {'name': 'Température moyenne', 'code': 'TEMP_AVG', 'unite': '°C', 'categorie': 'temperature', 'importance_agricole': 'critique', 'valeur_min': -50, 'valeur_max': 60},
            {'name': 'Température minimale', 'code': 'TEMP_MIN', 'unite': '°C', 'categorie': 'temperature', 'importance_agricole': 'critique', 'valeur_min': -50, 'valeur_max': 60},
            {'name': 'Température maximale', 'code': 'TEMP_MAX', 'unite': '°C', 'categorie': 'temperature', 'importance_agricole': 'critique', 'valeur_min': -50, 'valeur_max': 60},
            
            # Humidité
            {'name': 'Humidité relative', 'code': 'HUMIDITY', 'unite': '%', 'categorie': 'humidite', 'importance_agricole': 'elevee', 'valeur_min': 0, 'valeur_max': 100},
            {'name': 'Point de rosée', 'code': 'DEW_POINT', 'unite': '°C', 'categorie': 'humidite', 'importance_agricole': 'moyenne', 'valeur_min': -50, 'valeur_max': 60},
            
            # Précipitations
            {'name': 'Précipitations totales', 'code': 'PRECIP', 'unite': 'mm', 'categorie': 'precipitation', 'importance_agricole': 'critique', 'valeur_min': 0, 'valeur_max': 1000},
            {'name': 'Intensité des précipitations', 'code': 'PRECIP_INT', 'unite': 'mm/h', 'categorie': 'precipitation', 'importance_agricole': 'elevee', 'valeur_min': 0, 'valeur_max': 200},
            
            # Vent
            {'name': 'Vitesse du vent', 'code': 'WIND_SPEED', 'unite': 'km/h', 'categorie': 'vent', 'importance_agricole': 'moyenne', 'valeur_min': 0, 'valeur_max': 200},
            {'name': 'Direction du vent', 'code': 'WIND_DIR', 'unite': '°', 'categorie': 'vent', 'importance_agricole': 'faible', 'valeur_min': 0, 'valeur_max': 360},
            
            # Pression
            {'name': 'Pression atmosphérique', 'code': 'PRESSURE', 'unite': 'hPa', 'categorie': 'pression', 'importance_agricole': 'faible', 'valeur_min': 800, 'valeur_max': 1200},
            
            # Ensoleillement
            {'name': 'Durée d\'ensoleillement', 'code': 'SUNSHINE', 'unite': 'h', 'categorie': 'ensoleillement', 'importance_agricole': 'elevee', 'valeur_min': 0, 'valeur_max': 24},
            {'name': 'Rayonnement solaire', 'code': 'SOLAR_RAD', 'unite': 'W/m²', 'categorie': 'ensoleillement', 'importance_agricole': 'moyenne', 'valeur_min': 0, 'valeur_max': 1500},
        ]
        
        for param in parametres:
            if not self.search([('code', '=', param['code'])]):
                self.create(param)
