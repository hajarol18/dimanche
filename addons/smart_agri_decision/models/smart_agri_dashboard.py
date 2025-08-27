# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriDashboard(models.Model):
    """Tableau de bord"""

    _name = 'smart_agri_dashboard'
    _description = 'Tableau de Bord'
    _order = 'name'

    name = fields.Char('Nom du tableau de bord', required=True)
    description = fields.Text('Description')
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True)
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes')
