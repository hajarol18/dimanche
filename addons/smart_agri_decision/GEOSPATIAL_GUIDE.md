# Guide d'utilisation des fonctionnalités géospatiales

## Vue d'ensemble

Le module Smart Agri Decision intègre des fonctionnalités géospatiales avancées basées sur PostGIS et Leaflet.js pour la gestion et la visualisation des parcelles agricoles.

## Fonctionnalités principales

### 1. Gestion des données géospatiales

#### Champs géospatiaux disponibles
- **geo_point** : Point géographique (latitude/longitude)
- **geo_polygon** : Contour de la parcelle (polygone)
- **geo_area** : Surface calculée automatiquement (en hectares)
- **latitude/longitude** : Coordonnées géographiques classiques
- **altitude** : Altitude de la parcelle

#### Validation des coordonnées
- Latitude : -90° à +90°
- Longitude : -180° à +180°
- Précision : 8 décimales maximum

### 2. Import/Export GeoJSON

#### Import GeoJSON
1. Cliquer sur le bouton "Import GeoJSON" dans la vue parcelle
2. Sélectionner un fichier GeoJSON valide
3. Le système convertit automatiquement en format WKT
4. Les données géométriques sont stockées dans PostGIS

#### Export GeoJSON
1. Cliquer sur le bouton "Export GeoJSON" (disponible si géométrie définie)
2. Téléchargement automatique du fichier GeoJSON
3. Inclut toutes les propriétés de la parcelle

#### Format GeoJSON supporté
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[lon1, lat1], [lon2, lat2], ...]]
      },
      "properties": {
        "name": "Nom de la parcelle",
        "surface": 5.5,
        "type_sol": "Limoneux"
      }
    }
  ]
}
```

### 3. Carte interactive Leaflet

#### Affichage des parcelles
- **Polygones** : Affichés en bleu avec transparence
- **Points** : Marqueurs circulaires avec code de parcelle
- **Sélection** : Clic pour mettre en évidence une parcelle
- **Popup** : Informations détaillées de la parcelle

#### Contrôles de carte
- **Zoom** : Boutons +/- et molette de souris
- **Navigation** : Clic et glisser pour déplacer la carte
- **Centrage** : Double-clic sur une parcelle pour la centrer

#### Fonctionnalités avancées
- **Recherche** : Filtrage des parcelles par exploitation
- **Mesures** : Calcul automatique des surfaces
- **Export** : Sauvegarde de la vue carte

## Utilisation pratique

### Création d'une parcelle avec géométrie

1. **Saisie manuelle des coordonnées**
   ```
   Latitude: 46.603354
   Longitude: 1.888334
   ```

2. **Import depuis un fichier GeoJSON**
   - Préparer un fichier GeoJSON avec la géométrie
   - Utiliser le bouton "Import GeoJSON"
   - Vérifier la conversion automatique

3. **Dessin sur la carte**
   - Ouvrir la vue carte
   - Utiliser les outils de dessin
   - Sauvegarder la géométrie

### Visualisation des données

#### Vue liste
- Affichage des coordonnées
- Surface calculée automatiquement
- Statut géospatial (✓/✗)

#### Vue formulaire
- Onglet "Géolocalisation"
- Carte Leaflet intégrée
- Champs géospatiaux éditables

#### Vue carte
- Vue d'ensemble de toutes les parcelles
- Navigation interactive
- Filtrage et recherche

### Gestion des erreurs

#### Problèmes courants
1. **Coordonnées invalides**
   - Vérifier la plage (-90 à +90 pour lat, -180 à +180 pour lon)
   - Utiliser le bon format décimal

2. **Fichier GeoJSON invalide**
   - Vérifier la structure JSON
   - S'assurer que les coordonnées sont dans le bon ordre (longitude, latitude)

3. **Problèmes de projection**
   - Le système utilise WGS84 (EPSG:4326)
   - Convertir si nécessaire depuis d'autres systèmes

#### Solutions
- Validation automatique des coordonnées
- Messages d'erreur explicites
- Conversion automatique des formats

## Configuration technique

### Prérequis
- PostgreSQL avec extension PostGIS
- Module `base_geolocalize` activé
- Navigateur moderne avec support JavaScript ES6+

### Structure des fichiers
```
static/
├── src/
│   ├── css/
│   │   └── smart_agri.css
│   ├── js/
│   │   └── leaflet_map.js
│   └── lib/
│       └── leaflet/
│           └── leaflet.css
views/
├── parcelle_views.xml
├── geojson_wizard_views.xml
└── assets.xml
```

### Dépendances JavaScript
- Leaflet.js 1.9.4 (CDN)
- Odoo Web Framework
- Composants OWL

## Bonnes pratiques

### Données géospatiales
1. **Précision** : Utiliser une précision appropriée (5-10 mètres)
2. **Validation** : Vérifier les coordonnées avant import
3. **Métadonnées** : Documenter la source des données

### Performance
1. **Indexation** : Les champs géospatiaux sont automatiquement indexés
2. **Requêtes** : Utiliser les fonctions PostGIS pour les calculs complexes
3. **Cache** : La carte met en cache les données pour de meilleures performances

### Maintenance
1. **Sauvegarde** : Inclure les données PostGIS dans les sauvegardes
2. **Mise à jour** : Maintenir les extensions PostGIS à jour
3. **Monitoring** : Surveiller l'utilisation des ressources géospatiales

## Exemples d'utilisation

### Calcul de distance entre parcelles
```python
# Utilisation de PostGIS
distance = self.env.cr.execute("""
    SELECT ST_Distance(
        p1.geo_polygon::geography,
        p2.geo_polygon::geography
    ) FROM smart_agri_parcelle p1, smart_agri_parcelle p2
    WHERE p1.id = %s AND p2.id = %s
""", (parcelle1_id, parcelle2_id))
```

### Recherche de parcelles dans un rayon
```python
# Parcelles dans un rayon de 1km
parcelles_proches = self.env.cr.execute("""
    SELECT * FROM smart_agri_parcelle
    WHERE ST_DWithin(
        geo_point::geography,
        ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
        1000
    )
""", (longitude, latitude))
```

## Support et dépannage

### Logs et débogage
- Vérifier les logs Odoo pour les erreurs géospatiales
- Utiliser la console du navigateur pour les problèmes JavaScript
- Tester les requêtes PostGIS directement dans la base de données

### Ressources utiles
- [Documentation PostGIS](https://postgis.net/documentation/)
- [Documentation Leaflet](https://leafletjs.com/reference.html)
- [Spécifications GeoJSON](https://geojson.org/)

### Contact
Pour toute question ou problème, consulter la documentation du module ou contacter l'équipe de développement.
