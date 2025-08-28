# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SmartAgriParcelle(models.Model):
    """Parcelle agricole"""

    _name = 'smart_agri_parcelle'
    _description = 'Parcelle Agricole'
    _order = 'name'

    # RELATIONS PRINCIPALES - LOGIQUE MÉTIER
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True, ondelete='cascade')
    
    # Champs de base
    name = fields.Char('Nom de la parcelle', required=True)
    code = fields.Char('Code parcelle', required=True, size=20)
    description = fields.Text('Description')
    
    # Caractéristiques physiques
    surface = fields.Float('Surface (ha)', required=True, default=0.0)
    forme = fields.Selection([
        ('rectangulaire', 'Rectangulaire'),
        ('carree', 'Carrée'),
        ('irreguliere', 'Irrégulière'),
        ('autre', 'Autre')
    ], string='Forme', default='rectangulaire')
    
    # Localisation géographique (avec PostGIS)
    latitude = fields.Float('Latitude', digits=(16, 8))
    longitude = fields.Float('Longitude', digits=(16, 8))
    altitude = fields.Float('Altitude (m)')
    
    # Champs géospatiaux PostGIS (temporairement commentés pour éviter les erreurs)
    # geo_point = fields.GeoPoint(string='Localisation (point)', srid=4326)
    # geo_polygon = fields.GeoPolygon(string='Contour parcelle', srid=4326)
    # geo_area = fields.Float('Surface calculée (ha)', compute='_compute_geo_area', store=True)
    
    # Métadonnées géospatiales
    source_geo_data = fields.Selection([
        ('manual', 'Saisie manuelle'),
        ('import', 'Import fichier'),
        ('api', 'API externe'),
        ('gps', 'Relevé GPS')
    ], string='Source données géo', default='manual')
    precision_geo = fields.Float('Précision géométrique (m)', default=5.0)
    
    # Caractéristiques du sol
    type_sol_id = fields.Many2one('smart_agri_soil_type', string='Type de sol')
    ph = fields.Float('pH du sol')
    texture = fields.Selection([
        ('sableuse', 'Sableuse'),
        ('limoneuse', 'Limoneuse'),
        ('argileuse', 'Argileuse'),
        ('mixte', 'Mixte')
    ], string='Texture du sol')
    
    # Irrigation et drainage
    irrigation = fields.Boolean('Irrigation disponible')
    type_irrigation = fields.Selection([
        ('aspersion', 'Aspersion'),
        ('goutte_a_goutte', 'Goutte à goutte'),
        ('gravitaire', 'Gravitaire'),
        ('pivot', 'Pivot'),
        ('autre', 'Autre')
    ], string='Type d\'irrigation')
    drainage = fields.Boolean('Drainage disponible')
    
    # Statut et utilisation
    active = fields.Boolean('Actif', default=True)
    date_creation = fields.Date('Date de création', default=fields.Date.today, readonly=True)
    notes = fields.Text('Notes et observations')

    # CHAMPS CALCULÉS
    surface_utilisee = fields.Float('Surface utilisée (ha)', compute='_compute_surface_utilisee', store=True)
    culture_active_id = fields.Many2one('smart_agri_culture', string='Culture active', compute='_compute_culture_active', store=True)
    nombre_interventions = fields.Integer('Nombre d\'interventions', compute='_compute_nombre_interventions', store=True)
    
    # RELATIONS VERS LES AUTRES MODÈLES
    culture_ids = fields.One2many('smart_agri_culture', 'parcelle_id', string='Cultures')
    intervention_ids = fields.One2many('smart_agri_intervention', 'parcelle_id', string='Interventions')
    meteo_ids = fields.One2many('smart_agri_meteo', 'parcelle_id', string='Données météo')
    utilisation_intrant_ids = fields.One2many('smart_agri_utilisation_intrant', 'parcelle_id', string='Utilisations d\'intrants')
    
    @api.depends('surface')
    def _compute_surface_utilisee(self):
        """Calcule la surface utilisée (pour l'instant égale à la surface totale)"""
        for record in self:
            record.surface_utilisee = record.surface
    
    @api.depends('exploitation_id.culture_ids')
    def _compute_culture_active(self):
        """Trouve la culture active sur cette parcelle"""
        for record in self:
            if record.exploitation_id:
                culture_active = record.exploitation_id.culture_ids.filtered(
                    lambda c: c.parcelle_id.id == record.id and c.state == 'active'
                )
                record.culture_active_id = culture_active[0] if culture_active else False
            else:
                record.culture_active_id = False
    
    @api.depends('exploitation_id.intervention_ids')
    def _compute_nombre_interventions(self):
        """Calcule le nombre d'interventions sur cette parcelle"""
        for record in self:
            if record.exploitation_id:
                interventions = record.exploitation_id.intervention_ids.filtered(
                    lambda i: i.parcelle_id.id == record.id
                )
                record.nombre_interventions = len(interventions)
            else:
                record.nombre_interventions = 0
    
    # @api.depends('geo_polygon')
    # def _compute_geo_area(self):
    #     """Calcule la surface en hectares à partir du polygone géospatial"""
    #     for record in self:
    #         if record.geo_polygon:
    #             try:
    #                 # Utilisation de PostGIS pour calculer la surface
    #                 # La fonction ST_Area retourne la surface en m², conversion en hectares
    #                 # 1 hectare = 10000 m²
    #                 area_m2 = record.geo_polygon.area if hasattr(record.geo_polygon, 'area') else 0.0
    #                 record.geo_area = area_m2 / 10000 if area_m2 else 0.0
    #             except Exception:
    #                 record.geo_area = 0.0
    #         else:
    #             record.geo_area = 0.0
    
    # @api.onchange('latitude', 'longitude')
    # def _onchange_coordinates(self):
    #     """Met à jour le point géospatial quand les coordonnées changent"""
    #     for record in self:
    #         if record.latitude and record.longitude:
    #             record.geo_point = f'POINT({record.longitude} {record.latitude})'
    
    # @api.onchange('geo_point')
    # def _onchange_geo_point(self):
    #     """Met à jour les coordonnées quand le point géospatial change"""
    #     for record in self:
    #         if record.geo_point:
    #         # Extraction des coordonnées du point WKT
    #         point_wkt = record.geo_point.wkt
    #         if point_wkt and 'POINT' in point_wkt:
    #         # Format attendu: 'POINT(longitude latitude)'
    #         coords = point_wkt.replace('POINT(', '').replace(')', '').split()
    #         if len(coords) >= 2:
    #         record.longitude = float(coords[0])
    #         record.latitude = float(coords[1])

    # MÉTHODES D'IMPORT/EXPORT GÉOSPATIAL (temporairement commentées)
    
    # def action_import_geojson(self):
    #     """Action pour importer des données GeoJSON"""
    #     self.ensure_one()
    #     # Cette méthode sera appelée depuis l'interface utilisateur
    #     # Elle ouvrira un assistant pour importer un fichier GeoJSON
    #     return {
    #         'name': 'Import GeoJSON',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'smart_agri_geojson_wizard',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'context': {'default_parcelle_id': self.id}
    #     }
    
    # def action_export_geojson(self):
    #     """Action pour exporter les données au format GeoJSON"""
    #     self.ensure_one()
    #     
    #     # Vérification de la géométrie
    #     if not self.geo_polygon and not self.geo_point:
    #         raise ValidationError("Cette parcelle n'a pas de géométrie définie.")
    #     
    #     # Préparation des données GeoJSON
    #     geometry = None
    #     if self.geo_polygon:
    #         geometry = self.geo_polygon.geojson
    #     elif self.geo_point:
    #         geometry = self.geo_point.geojson
    #     
    #     # Création d'un Feature GeoJSON
    #     feature = {
    #         'type': 'Feature',
    #         'geometry': geometry,
    #         'properties': {
    #             'id': self.id,
    #             'name': self.name,
    #             'code': self.code,
    #             'surface': self.surface,
    #             'surface_geo': self.geo_area or 0.0,
    #             'exploitation': self.exploitation_id.name if self.exploitation_id else '',
    #             'type_sol': self.type_sol_id.name if self.type_sol_id else '',
    #             'forme': self.forme,
    #             'irrigation': self.irrigation,
    #             'drainage': self.drainage,
    #             'ph': self.ph,
    #             'texture': self.texture,
    #             'altitude': self.altitude,
    #             'source_geo_data': self.source_geo_data,
    #             'precision_geo': self.precision_geo,
    #             'date_creation': self.date_creation.isoformat() if self.date_creation else '',
    #         }
    #     }
    #     
    #     # Création d'un FeatureCollection GeoJSON
    #     feature_collection = {
    #         'type': 'FeatureCollection',
    #         'features': [feature]
    #     }
    #     
    #     # Retourne une action pour télécharger le fichier
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': '/web/content/smart_agri_parcelle/%s/geojson?download=true' % self.id,
    #         'target': 'self',
    #     }
    
    # ========================================
    # CONTRAINTES MÉTIER
    # ========================================
    
    @api.constrains('surface')
    def _check_surface_positive(self):
        """Vérifie que la surface de la parcelle est positive"""
        for record in self:
            if record.surface <= 0:
                raise ValidationError("La surface de la parcelle doit être strictement positive.")
    
    @api.constrains('surface', 'exploitation_id')
    def _check_surface_exploitation_coherence(self):
        """Vérifie que la surface de la parcelle ne dépasse pas la surface disponible de l'exploitation"""
        for record in self:
            if record.exploitation_id:
                # Calculer la surface déjà utilisée par les autres parcelles
                autres_parcelles = record.exploitation_id.parcelle_ids.filtered(lambda p: p.id != record.id)
                surface_utilisee = sum(autres_parcelles.mapped('surface'))
                surface_disponible = record.exploitation_id.surface_totale - surface_utilisee
                
                if record.surface > surface_disponible:
                    raise ValidationError(
                        f"La surface de la parcelle ({record.surface:.2f} ha) dépasse la surface disponible "
                        f"de l'exploitation ({surface_disponible:.2f} ha). "
                        f"Surface totale exploitation: {record.exploitation_id.surface_totale:.2f} ha, "
                        f"Surface déjà utilisée: {surface_utilisee:.2f} ha."
                    )
    
    @api.constrains('latitude', 'longitude')
    def _check_coordinates(self):
        """Vérifie la validité des coordonnées géographiques"""
        for record in self:
            if record.latitude and (record.latitude < -90 or record.latitude > 90):
                raise ValidationError('La latitude doit être comprise entre -90 et 90.')
            if record.longitude and (record.longitude < -180 or record.longitude > 180):
                raise ValidationError('La longitude doit être comprise entre -180 et 180.')

    # MÉTHODES MÉTIER
    def action_voir_cultures(self):
        """Action pour voir les cultures de cette parcelle"""
        return {
            'name': f'Cultures de {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_culture',
            'view_mode': 'list,form',
            'domain': [('parcelle_id', '=', self.id)],
            'context': {'default_parcelle_id': self.id, 'default_exploitation_id': self.exploitation_id.id},
        }
    
    def action_voir_interventions(self):
        """Action pour voir les interventions sur cette parcelle"""
        return {
            'name': f'Interventions sur {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_intervention',
            'view_mode': 'list,form',
            'domain': [('parcelle_id', '=', self.id)],
            'context': {'default_parcelle_id': self.id, 'default_exploitation_id': self.exploitation_id.id},
        }
    
    def action_voir_meteo(self):
        """Action pour voir les données météo de cette parcelle"""
        return {
            'name': f'Météo de {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_meteo',
            'view_mode': 'list,form',
            'domain': [('parcelle_id', '=', self.id)],
            'context': {'default_parcelle_id': self.id, 'default_exploitation_id': self.exploitation_id.id},
        }
    
    def action_voir_utilisation_intrants(self):
        """Action pour voir l'utilisation d'intrants sur cette parcelle"""
        return {
            'name': f'Utilisation d\'intrants sur {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_utilisation_intrant',
            'view_mode': 'list,form',
            'domain': [('parcelle_id', '=', self.id)],
            'context': {'default_parcelle_id': self.id, 'default_exploitation_id': self.exploitation_id.id},
        }
    
    # @api.model
    # def get_map_data(self, domain=None):
    #     """Récupère les données des parcelles pour l'affichage sur la carte"""
    #     if domain is None:
    #         domain = [('active', '=', True)]
    #     
    #     # Récupération des parcelles avec leurs données géospatiales
    #     parcelles = self.search(domain, fields=[
    #         'id', 'name', 'code', 'surface', 'geo_area', 'latitude', 'longitude',
    #         'geo_point', 'geo_polygon', 'exploitation_id', 'type_sol_id',
    #         'irrigation', 'drainage', 'ph', 'texture', 'altitude'
    #     ])
    #     
    #     map_data = []
    #     for parcelle in parcelles:
    #         # Préparation des données pour la carte
    #         parcelle_data = {
    #             'id': parcelle.id,
    #             'name': parcelle.name,
    #             'code': parcelle.code,
    #             'surface': parcelle.surface,
    #             'geo_area': parcelle.geo_area or 0.0,
    #             'latitude': parcelle.latitude,
    #             'longitude': parcelle.longitude,
    #             'exploitation': parcelle.exploitation_id.name if parcelle.exploitation_id else '',
    #             'type_sol': parcelle.type_sol_id.name if parcelle.type_sol_id else '',
    #             'irrigation': parcelle.irrigation,
    #             'drainage': parcelle.drainage,
    #             'ph': parcelle.ph,
    #             'texture': parcelle.texture,
    #             'altitude': parcelle.altitude,
    #         }
    #         
    #         # Ajout des données géospatiales
    #         if parcelle.geo_polygon:
    #             parcelle_data['geo_polygon'] = parcelle.geo_polygon.geojson
    #             parcelle_data['has_polygon'] = True
    #         elif parcelle.geo_point:
    #             parcelle_data['geo_point'] = parcelle.geo_point.geojson
    #             parcelle_data['has_polygon'] = False
    #         else:
    #             parcelle_data['has_polygon'] = False
    #         
    #         map_data.append(parcelle_data)
    #     
    #     return map_data
