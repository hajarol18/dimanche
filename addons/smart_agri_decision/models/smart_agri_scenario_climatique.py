# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriScenarioClimatique(models.Model):
    """Scénarios climatiques agricoles"""

    _name = 'smart_agri_scenario_climatique'
    _description = 'Scénarios Climatiques Agricoles'
    _order = 'name'

    # Champs de base
    name = fields.Char('Nom du scénario', required=True)
    description = fields.Text('Description')
    
    # Référence RCP
    rcp_scenario_id = fields.Many2one('smart_agri_rcp_scenario', string='Scénario RCP')
    
    # Impact agricole
    impact_rendement = fields.Selection([
        ('positif', 'Positif'),
        ('negatif', 'Négatif'),
        ('neutre', 'Neutre')
    ], string='Impact sur le rendement')
    
    # Adaptation
    strategies_adaptation = fields.Text('Stratégies d\'adaptation')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes')
