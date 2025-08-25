# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriRCPScenario(models.Model):
    """Scénarios RCP du GIEC"""

    _name = 'smart_agri_rcp_scenario'
    _description = 'Scénarios RCP du GIEC'
    _order = 'name'

    # Champs de base
    name = fields.Char('Nom du scénario', required=True)
    code = fields.Char('Code RCP', required=True, size=10)
    description = fields.Text('Description')
    
    # Caractéristiques du scénario
    type_scenario = fields.Selection([
        ('rcp26', 'RCP 2.6 - Optimiste'),
        ('rcp45', 'RCP 4.5 - Intermédiaire'),
        ('rcp60', 'RCP 6.0 - Intermédiaire élevé'),
        ('rcp85', 'RCP 8.5 - Pessimiste')
    ], string='Type de scénario', required=True)
    
    # Projections
    annee_2050 = fields.Float('Température 2050 (°C)')
    annee_2100 = fields.Float('Température 2100 (°C)')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes')
