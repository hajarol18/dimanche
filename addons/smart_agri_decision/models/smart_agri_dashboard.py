# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriDashboard(models.Model):
    """Tableau de bord agricole"""

    _name = 'smart_agri_dashboard'
    _description = 'Tableau de Bord Agricole'
    _order = 'name'

    # Champs de base
    name = fields.Char('Nom du tableau de bord', required=True)
    description = fields.Text('Description')
    
    # Type de dashboard
    type_dashboard = fields.Selection([
        ('exploitation', 'Exploitation'),
        ('parcelle', 'Parcelle'),
        ('culture', 'Culture'),
        ('meteo', 'Météo'),
        ('ia', 'Intelligence Artificielle')
    ], string='Type de tableau de bord', required=True)
    
    # Configuration
    config_affichage = fields.Text('Configuration d\'affichage')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes')
