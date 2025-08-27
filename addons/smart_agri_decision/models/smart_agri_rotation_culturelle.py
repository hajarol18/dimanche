# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SmartAgriRotationCulturelle(models.Model):
    """Gestion intelligente de la rotation culturelle avec objectifs"""

    _name = 'smart_agri_rotation_culturelle'
    _description = 'Plan de Rotation Culturelle Intelligent'
    _order = 'date_debut desc'
    _rec_name = 'name'

    # ========================================
    # CHAMPS D'IDENTIFICATION
    # ========================================
    name = fields.Char('Nom du plan de rotation', required=True)
    code = fields.Char('Code unique', required=True, copy=False)
    description = fields.Text('Description du plan de rotation')
    
    # ========================================
    # RELATIONS PRINCIPALES
    # ========================================
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True, ondelete='cascade')
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle', required=True, ondelete='cascade')
    
    # ========================================
    # PLANIFICATION TEMPORELLE
    # ========================================
    date_debut = fields.Date('Date de début', required=True, default=fields.Date.today)
    date_fin = fields.Date('Date de fin', required=True)
    duree_cycle = fields.Integer('Durée du cycle (années)', compute='_compute_duree_cycle', store=True)
    saison_courante = fields.Selection([
        ('printemps', 'Printemps'),
        ('ete', 'Été'),
        ('automne', 'Automne'),
        ('hiver', 'Hiver')
    ], string='Saison courante', compute='_compute_saison_courante', store=True)
    
    # ========================================
    # OBJECTIFS DE ROTATION
    # ========================================
    objectif_principal = fields.Selection([
        ('productivite', 'Maximiser la productivité'),
        ('durabilite', 'Améliorer la durabilité'),
        ('qualite', 'Optimiser la qualité'),
        ('resilience', 'Renforcer la résilience climatique'),
        ('economie', 'Réduire les coûts'),
        ('biodiversite', 'Préserver la biodiversité')
    ], string='Objectif principal', required=True, default='productivite')
    
    objectifs_secondaires = fields.Many2many('smart_agri_objectif_rotation', string='Objectifs secondaires')
    priorite_rotation = fields.Selection([
        ('critique', 'Critique'),
        ('elevee', 'Élevée'),
        ('normale', 'Normale'),
        ('faible', 'Faible')
    ], string='Priorité de rotation', default='normale')
    
    # ========================================
    # CULTURES DE ROTATION
    # ========================================
    culture_actuelle_id = fields.Many2one('smart_agri_culture', string='Culture actuelle', domain="[('exploitation_id', '=', exploitation_id)]")
    culture_precedente_id = fields.Many2one('smart_agri_culture', string='Culture précédente', domain="[('exploitation_id', '=', exploitation_id)]")
    culture_suivante_id = fields.Many2one('smart_agri_culture', string='Culture suivante recommandée', domain="[('exploitation_id', '=', exploitation_id)]")
    
    # ========================================
    # ANALYSE IA DE LA ROTATION
    # ========================================
    score_rotation = fields.Float('Score de rotation (%)', compute='_compute_score_rotation', store=True)
    benefices_rotation = fields.Text('Bénéfices de la rotation')
    risques_rotation = fields.Text('Risques identifiés')
    recommandations_ia = fields.Text('Recommandations IA')
    
    # ========================================
    # SUIVI ET PERFORMANCE
    # ========================================
    rendement_attendu = fields.Float('Rendement attendu (t/ha)')
    rendement_reel = fields.Float('Rendement réel (t/ha)')
    ecart_rendement = fields.Float('Écart de rendement (%)', compute='_compute_ecart_rendement', store=True)
    
    # ========================================
    # STATUT ET SUIVI
    # ========================================
    state = fields.Selection([
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('suspendu', 'Suspendu'),
        ('annule', 'Annulé')
    ], string='État', default='planifie')
    
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes et observations')
    
    # ========================================
    # MÉTHODES CALCULÉES
    # ========================================
    
    @api.depends('date_debut', 'date_fin')
    def _compute_duree_cycle(self):
        """Calcule la durée du cycle de rotation"""
        for record in self:
            if record.date_debut and record.date_fin:
                delta = record.date_fin - record.date_debut
                record.duree_cycle = delta.days // 365
            else:
                record.duree_cycle = 0
    
    @api.depends('date_debut')
    def _compute_saison_courante(self):
        """Détermine la saison courante basée sur la date de début"""
        for record in self:
            if record.date_debut:
                month = record.date_debut.month
                if month in [3, 4, 5]:
                    record.saison_courante = 'printemps'
                elif month in [6, 7, 8]:
                    record.saison_courante = 'ete'
                elif month in [9, 10, 11]:
                    record.saison_courante = 'automne'
                else:
                    record.saison_courante = 'hiver'
            else:
                record.saison_courante = False
    
    @api.depends('rendement_attendu', 'rendement_reel')
    def _compute_ecart_rendement(self):
        """Calcule l'écart entre rendement attendu et réel"""
        for record in self:
            if record.rendement_attendu and record.rendement_reel:
                if record.rendement_attendu > 0:
                    record.ecart_rendement = ((record.rendement_reel - record.rendement_attendu) / record.rendement_attendu) * 100
                else:
                    record.ecart_rendement = 0
            else:
                record.ecart_rendement = 0
    
    @api.depends('culture_actuelle_id', 'culture_precedente_id', 'culture_suivante_id', 'objectif_principal')
    def _compute_score_rotation(self):
        """Calcule le score de rotation basé sur plusieurs critères"""
        for record in self:
            score = 0
            
            # Score basé sur la diversité des cultures
            cultures = set()
            if record.culture_actuelle_id:
                cultures.add(record.culture_actuelle_id.id)
            if record.culture_precedente_id:
                cultures.add(record.culture_precedente_id.id)
            if record.culture_suivante_id:
                cultures.add(record.culture_suivante_id.id)
            
            diversite = len(cultures)
            if diversite >= 3:
                score += 40
            elif diversite == 2:
                score += 25
            else:
                score += 10
            
            # Score basé sur l'objectif principal
            if record.objectif_principal == 'durabilite':
                score += 30
            elif record.objectif_principal == 'biodiversite':
                score += 25
            elif record.objectif_principal == 'resilience':
                score += 20
            else:
                score += 15
            
            # Score basé sur la priorité
            if record.priorite_rotation == 'critique':
                score += 20
            elif record.priorite_rotation == 'elevee':
                score += 15
            elif record.priorite_rotation == 'normale':
                score += 10
            else:
                score += 5
            
            record.score_rotation = min(score, 100)  # Plafonné à 100%
    
    # ========================================
    # MÉTHODES MÉTIER
    # ========================================
    
    def action_demarrer_rotation(self):
        """Démarre la rotation culturelle"""
        self.ensure_one()
        if self.state == 'planifie':
            self.write({
                'state': 'en_cours',
                'date_debut': fields.Date.today()
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Rotation démarrée',
                    'message': f'La rotation {self.name} a été démarrée avec succès.',
                    'type': 'success'
                }
            }
    
    def action_terminer_rotation(self):
        """Termine la rotation culturelle"""
        self.ensure_one()
        if self.state == 'en_cours':
            self.write({
                'state': 'termine',
                'date_fin': fields.Date.today()
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Rotation terminée',
                    'message': f'La rotation {self.name} a été terminée avec succès.',
                    'type': 'success'
                }
            }
    
    def action_suspendre_rotation(self):
        """Suspend la rotation culturelle"""
        self.ensure_one()
        if self.state in ['planifie', 'en_cours']:
            self.write({'state': 'suspendu'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Rotation suspendue',
                    'message': f'La rotation {self.name} a été suspendue.',
                    'type': 'warning'
                }
            }
    
    def action_planifier_suivante(self):
        """Planifie la culture suivante de la rotation"""
        self.ensure_one()
        if self.culture_suivante_id:
            # Créer une nouvelle rotation pour la culture suivante
            nouvelle_rotation = self.copy({
                'name': f'Rotation {self.culture_suivante_id.name} - {self.parcelle_id.name}',
                'culture_actuelle_id': self.culture_suivante_id.id,
                'culture_precedente_id': self.culture_actuelle_id.id,
                'culture_suivante_id': False,
                'date_debut': fields.Date.today(),
                'date_fin': fields.Date.today() + timedelta(days=365),
                'state': 'planifie'
            })
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'smart_agri_rotation_culturelle',
                'res_id': nouvelle_rotation.id,
                'view_mode': 'form',
                'target': 'current'
            }
    
    # ========================================
    # CONTRAINTES ET VALIDATIONS
    # ========================================
    
    @api.constrains('date_debut', 'date_fin')
    def _check_dates_rotation(self):
        """Vérifie la cohérence des dates de rotation"""
        for record in self:
            if record.date_debut and record.date_fin:
                if record.date_debut >= record.date_fin:
                    raise ValidationError("La date de début doit être antérieure à la date de fin.")
    
    @api.constrains('culture_actuelle_id', 'culture_precedente_id')
    def _check_cultures_differentes(self):
        """Vérifie que les cultures sont différentes"""
        for record in self:
            if (record.culture_actuelle_id and record.culture_precedente_id and 
                record.culture_actuelle_id.id == record.culture_precedente_id.id):
                raise ValidationError("La culture actuelle ne peut pas être identique à la culture précédente.")
    
    # ========================================
    # MÉTHODES DE RECHERCHE
    # ========================================
    
    @api.model
    def _search_rotations_prioritaires(self, operator, value):
        """Recherche les rotations prioritaires"""
        domain = [('priorite_rotation', 'in', ['critique', 'elevee'])]
        return domain
    
    @api.model
    def _search_rotations_en_cours(self, operator, value):
        """Recherche les rotations en cours"""
        domain = [('state', '=', 'en_cours')]
        return domain


class SmartAgriObjectifRotation(models.Model):
    """Objectifs de rotation culturelle"""
    
    _name = 'smart_agri_objectif_rotation'
    _description = 'Objectifs de Rotation Culturelle'
    
    name = fields.Char('Nom de l\'objectif', required=True)
    code = fields.Char('Code', required=True)
    description = fields.Text('Description')
    categorie = fields.Selection([
        ('agronomique', 'Agronomique'),
        ('economique', 'Économique'),
        ('environnemental', 'Environnemental'),
        ('social', 'Social')
    ], string='Catégorie')
    
    priorite = fields.Selection([
        ('critique', 'Critique'),
        ('elevee', 'Élevée'),
        ('normale', 'Normale'),
        ('faible', 'Faible')
    ], string='Priorité', default='normale')
    
    indicateurs = fields.Text('Indicateurs de suivi')
    actions_concretes = fields.Text('Actions concrètes à mettre en place')
