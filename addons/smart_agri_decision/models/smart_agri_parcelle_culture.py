# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SmartAgriParcelleCulture(models.Model):
    """Relation entre parcelles et cultures"""

    _name = 'smart_agri_parcelle_culture'
    _description = 'Relation Parcelle-Culture'
    _order = 'date_plantation desc'

    # RELATIONS PRINCIPALES
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle', required=True, ondelete='cascade')
    culture_id = fields.Many2one('smart_agri_culture', string='Culture', required=True, ondelete='cascade')
    
    # DATES DE CULTURE
    date_plantation = fields.Date('Date de plantation', required=True)
    date_recolte_prevue = fields.Date('Date de récolte prévue')
    date_recolte_reelle = fields.Date('Date de récolte réelle')
    
    # ÉTAT ET RENDEMENT
    etat_culture = fields.Selection([
        ('planifiee', 'Planifiée'),
        ('en_croissance', 'En croissance'),
        ('en_production', 'En production'),
        ('recoltee', 'Récoltée'),
        ('abandonnee', 'Abandonnée')
    ], string='État de la culture', default='planifiee', required=True)
    
    rendement_obtenu = fields.Float('Rendement obtenu (t/ha)', default=0.0)
    
    # NOTES ET OBSERVATIONS
    notes = fields.Text('Notes')
    
    # Statut
    active = fields.Boolean('Actif', default=True)

    # CHAMPS CALCULÉS
    duree_culture = fields.Integer('Durée de culture (jours)', compute='_compute_duree_culture', store=True)
    rendement_total = fields.Float('Rendement total (t)', compute='_compute_rendement_total', store=True)
    
    @api.depends('date_plantation', 'date_recolte_reelle')
    def _compute_duree_culture(self):
        """Calcule la durée réelle de la culture"""
        for relation in self:
            if relation.date_plantation and relation.date_recolte_reelle:
                delta = relation.date_recolte_reelle - relation.date_plantation
                relation.duree_culture = delta.days
            else:
                relation.duree_culture = 0
    
    @api.depends('rendement_obtenu', 'parcelle_id.surface')
    def _compute_rendement_total(self):
        """Calcule le rendement total"""
        for relation in self:
            if relation.parcelle_id and relation.rendement_obtenu:
                relation.rendement_total = relation.rendement_obtenu * relation.parcelle_id.surface
            else:
                relation.rendement_total = 0.0

    # CONTRAINTES MÉTIER
    @api.constrains('date_plantation', 'date_recolte_prevue')
    def _check_dates_culture(self):
        """Vérifie la cohérence des dates de culture"""
        for relation in self:
            if relation.date_plantation and relation.date_recolte_prevue:
                if relation.date_plantation >= relation.date_recolte_prevue:
                    raise ValidationError('La date de plantation doit être antérieure à la date de récolte prévue.')
    
    @api.constrains('parcelle_id', 'culture_id')
    def _check_relation_unique(self):
        """Vérifie qu'une parcelle ne peut pas avoir la même culture en même temps"""
        for relation in self:
            if relation.parcelle_id and relation.culture_id:
                # Vérifier s'il existe déjà une relation active pour cette parcelle et culture
                existing = self.search([
                    ('parcelle_id', '=', relation.parcelle_id.id),
                    ('culture_id', '=', relation.culture_id.id),
                    ('active', '=', True),
                    ('id', '!=', relation.id)
                ])
                if existing:
                    raise ValidationError(
                        f'La parcelle {relation.parcelle_id.name} a déjà la culture {relation.culture_id.name} en cours.'
                    )

    # MÉTHODES MÉTIER
    def action_demarrer_culture(self):
        """Action pour démarrer la culture"""
        self.ensure_one()
        if self.etat_culture == 'planifiee':
            self.write({'etat_culture': 'en_croissance'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Culture démarrée !',
                    'message': f'La culture {self.culture_id.name} a été démarrée sur la parcelle {self.parcelle_id.name}.',
                    'type': 'success',
                }
            }
    
    def action_recolter_culture(self):
        """Action pour récolter la culture"""
        self.ensure_one()
        if self.etat_culture in ['en_croissance', 'en_production']:
            self.write({'etat_culture': 'recoltee'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Culture récoltée !',
                    'message': f'La culture {self.culture_id.name} a été récoltée sur la parcelle {self.parcelle_id.name}.',
                    'type': 'success',
                }
            }
    
    def action_abandonner_culture(self):
        """Action pour abandonner la culture"""
        self.ensure_one()
        if self.etat_culture in ['planifiee', 'en_croissance', 'en_production']:
            self.write({'etat_culture': 'abandonnee'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Culture abandonnée !',
                    'message': f'La culture {self.culture_id.name} a été abandonnée sur la parcelle {self.parcelle_id.name}.',
                    'type': 'warning',
                }
            }

    def name_get(self):
        """Nom d'affichage personnalisé"""
        result = []
        for record in self:
            name = f"{record.parcelle_id.name} - {record.culture_id.name}"
            result.append((record.id, name))
        return result
