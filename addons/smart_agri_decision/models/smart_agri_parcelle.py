# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriParcelle(models.Model):
    """Parcelle agricole"""

    _name = 'smart_agri_parcelle'
    _description = 'Parcelle Agricole'
    _order = 'name'

    # Champs de base
    name = fields.Char('Nom de la parcelle', required=True)
    code = fields.Char('Code', required=True, size=20)
    description = fields.Text('Description')
    
    # Surface et localisation
    surface = fields.Float('Surface (ha)', required=True, default=0.0)
    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')
    
    # Type de sol (référence simple)
    soil_type_id = fields.Many2one('smart_agri_soil_type', string='Type de sol')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes')
    
    # Date de création
    date_creation = fields.Date('Date de création', default=fields.Date.today)
