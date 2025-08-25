# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriCulture(models.Model):
    """Culture agricole"""

    _name = 'smart_agri_culture'
    _description = 'Culture Agricole'
    _order = 'name'

    # Champs de base
    name = fields.Char('Nom de la culture', required=True)
    code = fields.Char('Code', required=True, size=20)
    description = fields.Text('Description')
    
    # Caractéristiques de la culture
    famille = fields.Selection([
        ('cereales', 'Céréales'),
        ('legumineuses', 'Légumineuses'),
        ('oleagineux', 'Oléagineux'),
        ('fruits', 'Fruits'),
        ('legumes', 'Légumes'),
        ('autres', 'Autres')
    ], string='Famille', required=True)
    
    # Cycle de culture
    duree_cycle = fields.Integer('Durée du cycle (jours)', default=0)
    saison_plantation = fields.Selection([
        ('printemps', 'Printemps'),
        ('ete', 'Été'),
        ('automne', 'Automne'),
        ('hiver', 'Hiver'),
        ('toute_annee', 'Toute l\'année')
    ], string='Saison de plantation')
    
    # Rendement
    rendement_moyen = fields.Float('Rendement moyen (t/ha)', default=0.0)
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes')
