# -*- coding: utf-8 -*-

from odoo import models, fields


class TestModel(models.Model):
    """Modèle de test ultra-simple"""
    
    _name = 'test.model'
    _description = 'Modèle de test'
    
    name = fields.Char('Nom', required=True)
    description = fields.Text('Description')
