# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriSoilType(models.Model):
    """Type de sol avec propriétés agronomiques détaillées"""
    
    _name = 'smart_agri_soil_type'
    _description = 'Type de sol'
    _order = 'name'
    
    # Champs de base
    name = fields.Char('Nom du type de sol', required=True)
    code = fields.Char('Code', required=True, size=20)
    description = fields.Text('Description')
    
    # Propriétés physiques
    water_retention = fields.Float('Rétention d\'eau (%)', default=0.0)
    drainage = fields.Float('Drainage (%)', default=0.0)
    fertility = fields.Float('Fertilité (%)', default=0.0)
    
    # Propriétés chimiques
    ph_min = fields.Float('pH minimum', default=6.0)
    ph_max = fields.Float('pH maximum', default=7.0)
    organic_matter = fields.Float('Matière organique (%)', default=2.0)
    
    # Couleur
    color = fields.Char('Couleur', default='#808080')
