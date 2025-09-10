# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SmartAgriCulture(models.Model):
    """Culture agricole"""

    _name = 'smart_agri_culture'
    _description = 'Culture Agricole'
    _order = 'name'

    # RELATIONS PRINCIPALES - LOGIQUE MÉTIER
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=False, ondelete='cascade')
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle', required=False, ondelete='cascade')
    
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
    
    # SURFACE ET PLANIFICATION
    surface_utilisee = fields.Float('Surface utilisée (ha)', required=True, default=0.0)
    date_plantation = fields.Date('Date de plantation')
    date_recolte_prevue = fields.Date('Date de récolte prévue')
    date_recolte_reelle = fields.Date('Date de récolte réelle')
    
    # ÉTAT DE LA CULTURE
    state = fields.Selection([
        ('planifiee', 'Planifiée'),
        ('active', 'En cours'),
        ('recoltee', 'Récoltée'),
        ('abandonnee', 'Abandonnée')
    ], string='État', default='planifiee', required=True)
    
    # RENDEMENT RÉEL
    rendement_reel = fields.Float('Rendement réel (t/ha)', default=0.0)
    qualite_recolte = fields.Selection([
        ('excellente', 'Excellente'),
        ('bonne', 'Bonne'),
        ('moyenne', 'Moyenne'),
        ('mauvaise', 'Mauvaise')
    ], string='Qualité de la récolte')
    
    # NOTES ET OBSERVATIONS
    observations = fields.Text('Observations')
    problemes_rencontres = fields.Text('Problèmes rencontrés')
    solutions_appliquees = fields.Text('Solutions appliquées')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes')

    # CHAMPS CALCULÉS
    duree_culture = fields.Integer('Durée de culture (jours)', compute='_compute_duree_culture', store=True)
    rendement_total = fields.Float('Rendement total (t)', compute='_compute_rendement_total', store=True)
    nombre_interventions = fields.Integer('Nombre d\'interventions', compute='_compute_nombre_interventions', store=True)
    
    @api.depends('date_plantation', 'date_recolte_reelle')
    def _compute_duree_culture(self):
        """Calcule la durée réelle de la culture"""
        for culture in self:
            if culture.date_plantation and culture.date_recolte_reelle:
                delta = culture.date_recolte_reelle - culture.date_plantation
                culture.duree_culture = delta.days
            else:
                culture.duree_culture = 0
    
    @api.depends('rendement_reel', 'surface_utilisee')
    def _compute_rendement_total(self):
        """Calcule le rendement total"""
        for culture in self:
            culture.rendement_total = culture.rendement_reel * culture.surface_utilisee
    
    @api.depends('exploitation_id.intervention_ids')
    def _compute_nombre_interventions(self):
        """Calcule le nombre d'interventions sur cette culture"""
        for culture in self:
            if culture.exploitation_id:
                interventions = self.env['smart_agri_intervention'].search([
                    ('culture_id', '=', culture.id),
                    ('active', '=', True)
                ])
                culture.nombre_interventions = len(interventions)
            else:
                culture.nombre_interventions = 0
    
    # ========================================
    # NOUVELLES MÉTHODES MÉTIER INTELLIGENTES
    # ========================================
    
    def optimiser_rotation_suivante(self):
        """Recommandation IA pour la culture suivante optimale"""
        self.ensure_one()
        
        # Logique métier : Recommandation basée sur la famille et l'historique
        if self.famille == 'cereales':
            # Après céréales, recommander légumineuses pour l'azote
            cultures_recommandees = self.env['smart_agri_culture'].search([
                ('famille', '=', 'legumineuses'),
                ('active', '=', True)
            ])
        elif self.famille == 'legumineuses':
            # Après légumineuses, recommander céréales
            cultures_recommandees = self.env['smart_agri_culture'].search([
                ('famille', '=', 'cereales'),
                ('active', '=', True)
            ])
        else:
            # Pour les autres familles, diversification
            cultures_recommandees = self.env['smart_agri_culture'].search([
                ('famille', '!=', self.famille),
                ('active', '=', True)
            ])
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cultures Recommandées',
            'res_model': 'smart_agri_culture',
            'view_mode': 'list,form',
            'domain': [('id', 'in', cultures_recommandees.ids)],
            'target': 'new'
        }

    # CONTRAINTES MÉTIER
    @api.constrains('surface_utilisee')
    def _check_surface_positive(self):
        """Vérifie que la surface utilisée est positive"""
        for culture in self:
            if culture.surface_utilisee <= 0:
                raise ValidationError('La surface utilisée doit être strictement positive.')
    
    @api.constrains('surface_utilisee', 'parcelle_id')
    def _check_surface_parcelle(self):
        """Vérifie que la surface utilisée ne dépasse pas celle de la parcelle"""
        for culture in self:
            if culture.parcelle_id and culture.surface_utilisee > culture.parcelle_id.surface:
                raise ValidationError(
                    f'La surface utilisée ({culture.surface_utilisee} ha) ne peut pas dépasser '
                    f'celle de la parcelle ({culture.parcelle_id.surface} ha).'
                )
    
    @api.constrains('date_plantation', 'date_recolte_prevue')
    def _check_dates_culture(self):
        """Vérifie la cohérence des dates de culture"""
        for culture in self:
            if culture.date_plantation and culture.date_recolte_prevue:
                if culture.date_plantation >= culture.date_recolte_prevue:
                    raise ValidationError('La date de plantation doit être antérieure à la date de récolte prévue.')

    # MÉTHODES MÉTIER
    def action_voir_interventions(self):
        """Action pour voir les interventions sur cette culture"""
        return {
            'name': f'Interventions sur {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_intervention',
            'view_mode': 'list,form',
            'domain': [('culture_id', '=', self.id)],
            'context': {'default_culture_id': self.id, 'default_exploitation_id': self.exploitation_id.id, 'default_parcelle_id': self.parcelle_id.id},
        }
    
    def action_voir_utilisation_intrants(self):
        """Action pour voir l'utilisation d'intrants pour cette culture"""
        return {
            'name': f'Utilisation d\'intrants pour {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_utilisation_intrant',
            'view_mode': 'list,form',
            'domain': [('culture_id', '=', self.id)],
            'context': {'default_culture_id': self.id, 'default_exploitation_id': self.exploitation_id.id, 'default_parcelle_id': self.parcelle_id.id},
        }
    
    def action_demarrer_culture(self):
        """Action pour démarrer la culture"""
        self.ensure_one()
        if self.state == 'planifiee':
            self.write({'state': 'active'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Culture démarrée !',
                    'message': f'La culture {self.name} a été démarrée.',
                    'type': 'success',
                }
            }
    
    def action_recolter_culture(self):
        """Action pour récolter la culture"""
        self.ensure_one()
        if self.state == 'active':
            self.write({'state': 'recoltee'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Culture récoltée !',
                    'message': f'La culture {self.name} a été récoltée.',
                    'type': 'success',
                }
            }
    
    def action_abandonner_culture(self):
        """Action pour abandonner la culture"""
        self.ensure_one()
        if self.state in ['planifiee', 'active']:
            self.write({'state': 'abandonnee'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Culture abandonnée !',
                    'message': f'La culture {self.name} a été abandonnée.',
                    'type': 'warning',
                }
            }
