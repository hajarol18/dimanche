# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriObjectifRotation(models.Model):
    """Objectif de rotation"""

    _name = 'smart_agri_objectif_rotation'
    _description = 'Objectif de Rotation'
    _order = 'name'

    name = fields.Char('Nom de l\'objectif', required=True)
    description = fields.Text('Description')
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True)
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes')
