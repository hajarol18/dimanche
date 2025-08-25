# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriObjectifRotation(models.Model):
    """Objectifs de rotation"""

    _name = 'smart_agri_objectif_rotation'
    _description = 'Objectifs de Rotation'
    _order = 'name'

    # Champs de base
    name = fields.Char('Nom de l\'objectif', required=True)
    description = fields.Text('Description')
    
    # Type d'objectif
    type_objectif = fields.Selection([
        ('rendement', 'Amélioration du rendement'),
        ('qualite', 'Amélioration de la qualité'),
        ('durabilite', 'Durabilité des sols'),
        ('economique', 'Optimisation économique'),
        ('environnemental', 'Impact environnemental')
    ], string='Type d\'objectif', required=True)
    
    # Cible
    valeur_cible = fields.Float('Valeur cible')
    unite = fields.Char('Unité')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes')
