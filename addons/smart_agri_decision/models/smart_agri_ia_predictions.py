# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriIAPredictions(models.Model):
    """Prédictions IA pour l'agriculture"""

    _name = 'smart_agri_ia_predictions'
    _description = 'Prédictions IA Agricoles'
    _order = 'date_creation desc'

    # Champs de base
    name = fields.Char('Nom de la prédiction', required=True)
    description = fields.Text('Description')
    date_creation = fields.Datetime('Date de création', default=fields.Datetime.now)
    
    # Type de prédiction
    type_prediction = fields.Selection([
        ('rendement', 'Prédiction de rendement'),
        ('culture_optimale', 'Culture optimale'),
        ('risque_climatique', 'Risque climatique'),
        ('irrigation', 'Optimisation irrigation'),
        ('engrais', 'Optimisation engrais')
    ], string='Type de prédiction', required=True)
    
    # Données d'entrée
    donnees_entree = fields.Text('Données d\'entrée')
    
    # Résultats
    resultat = fields.Text('Résultat de la prédiction')
    confiance = fields.Float('Niveau de confiance (%)', default=0.0)
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes')
