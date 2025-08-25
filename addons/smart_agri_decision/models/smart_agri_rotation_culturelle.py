# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriRotationCulturelle(models.Model):
    """Rotation culturelle"""

    _name = 'smart_agri_rotation_culturelle'
    _description = 'Rotation Culturelle'
    _order = 'name'

    # Champs de base
    name = fields.Char('Nom de la rotation', required=True)
    description = fields.Text('Description')
    
    # Planification
    annee_debut = fields.Integer('Année de début', required=True)
    duree_rotation = fields.Integer('Durée de rotation (années)', default=4)
    
    # Cultures de la rotation
    culture_1 = fields.Char('Culture année 1')
    culture_2 = fields.Char('Culture année 2')
    culture_3 = fields.Char('Culture année 3')
    culture_4 = fields.Char('Culture année 4')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes')
