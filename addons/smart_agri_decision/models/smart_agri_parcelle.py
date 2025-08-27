# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


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
    
    # Localisation géographique (sans PostGIS)
    latitude = fields.Float('Latitude', digits=(16, 8))
    longitude = fields.Float('Longitude', digits=(16, 8))
    altitude = fields.Float('Altitude (m)')
    
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

    # CONTRAINTES MÉTIER
    @api.constrains('surface')
    def _check_surface_positive(self):
        """Vérifie que la surface est positive"""
        for record in self:
            if record.surface <= 0:
                raise ValidationError('La surface doit être strictement positive.')
    
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
