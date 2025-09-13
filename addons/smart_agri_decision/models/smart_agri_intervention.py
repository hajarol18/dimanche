# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SmartAgriIntervention(models.Model):
    """Intervention agricole - Planification complète"""

    _name = 'smart_agri_intervention'
    _description = 'Intervention Agricole'
    _order = 'date_planifiee'

    # RELATIONS PRINCIPALES - LOGIQUE MÉTIER
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True, ondelete='cascade')
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle', required=True, ondelete='cascade')
    culture_id = fields.Many2one('smart_agri_culture', string='Culture concernée', ondelete='cascade')
    
    # Champs de base
    name = fields.Char('Nom de l\'intervention', required=True)
    description = fields.Text('Description détaillée')
    
    # Type d'intervention détaillé
    type_intervention = fields.Selection([
        ('semis', 'Semis'),
        ('irrigation', 'Irrigation'),
        ('traitement', 'Traitement phytosanitaire'),
        ('recolte', 'Récolte'),
        ('fertilisation', 'Fertilisation'),
        ('labour', 'Labour'),
        ('desherbage', 'Désherbage'),
        ('taille', 'Taille'),
        ('greffage', 'Greffage'),
        ('autre', 'Autre')
    ], string='Type d\'intervention', required=True)
    
    # Planification temporelle
    date_planifiee = fields.Date('Date planifiée', required=True)
    date_execution = fields.Date('Date d\'exécution')
    duree_estimee = fields.Float('Durée estimée (heures)', default=1.0)
    
    # Statut et suivi
    state = fields.Selection([
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
        ('retardee', 'Retardée')
    ], string='État', default='planifiee')
    
    # Ressources et coûts
    main_oeuvre_requise = fields.Float('Main d\'œuvre requise (heures)')
    cout_estime = fields.Float('Coût estimé (€)')
    cout_reel = fields.Float('Coût réel (€)')
    
    # Conditions météorologiques
    conditions_meteo = fields.Text('Conditions météo requises')
    temperature_min = fields.Float('Température minimum (°C)')
    temperature_max = fields.Float('Température maximum (°C)')
    humidite_min = fields.Float('Humidité minimum (%)')
    
    # Notes et observations
    notes = fields.Text('Notes et observations')
    resultats = fields.Text('Résultats obtenus')
    problemes_rencontres = fields.Text('Problèmes rencontrés')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    
    # Calcul automatique du nom
    @api.depends('type_intervention', 'parcelle_id', 'date_planifiee')
    def _compute_name(self):
        for record in self:
            if record.type_intervention and record.parcelle_id and record.date_planifiee:
                record.name = f"{record.type_intervention.title()} - {record.parcelle_id.name} - {record.date_planifiee}"
            elif record.type_intervention:
                record.name = f"{record.type_intervention.title()} - {record.date_planifiee}"
            else:
                record.name = "Nouvelle intervention"

    # MÉTHODES MÉTIER
    def action_demarrer_intervention(self):
        """Action pour démarrer l'intervention"""
        self.ensure_one()
        if self.state == 'planifiee':
            self.write({
                'state': 'en_cours',
                'date_execution': fields.Date.today()
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Intervention démarrée !',
                    'message': f'L\'intervention {self.name} a été démarrée.',
                    'type': 'success',
                }
            }
    
    def action_terminer_intervention(self):
        """Action pour terminer l'intervention"""
        self.ensure_one()
        if self.state == 'en_cours':
            self.write({'state': 'terminee'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Intervention terminée !',
                    'message': f'L\'intervention {self.name} a été terminée.',
                    'type': 'success',
                }
            }
    
    def action_annuler_intervention(self):
        """Action pour annuler l'intervention"""
        self.ensure_one()
        if self.state in ['planifiee', 'en_cours']:
            self.write({'state': 'annulee'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Intervention annulée !',
                    'message': f'L\'intervention {self.name} a été annulée.',
                    'type': 'warning',
                }
            }
    
    def action_retarder_intervention(self):
        """Action pour retarder l'intervention"""
        self.ensure_one()
        if self.state == 'planifiee':
            self.write({'state': 'retardee'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Intervention retardée !',
                    'message': f'L\'intervention {self.name} a été retardée.',
                    'type': 'warning',
                }
            }
    
    def action_voir_utilisation_intrants(self):
        """Action pour voir l'utilisation d'intrants pour cette intervention"""
        return {
            'name': f'Utilisation d\'intrants pour {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_utilisation_intrant',
            'view_mode': 'list,form',
            'domain': [('intervention_id', '=', self.id)],
            'context': {'default_intervention_id': self.id, 'default_exploitation_id': self.exploitation_id.id, 'default_parcelle_id': self.parcelle_id.id, 'default_culture_id': self.culture_id.id},
        }

    # CONTRAINTES MÉTIER
    @api.constrains('date_planifiee', 'date_execution')
    def _check_dates_intervention(self):
        """Vérifie la cohérence des dates d'intervention"""
        for record in self:
            if record.date_execution and record.date_planifiee:
                if record.date_execution < record.date_planifiee:
                    raise ValidationError('La date d\'exécution ne peut pas être antérieure à la date planifiée.')
    
    @api.constrains('cout_estime', 'cout_reel')
    def _check_couts_positifs(self):
        """Vérifie que les coûts sont positifs"""
        for record in self:
            if record.cout_estime and record.cout_estime < 0:
                raise ValidationError('Le coût estimé doit être positif.')
            if record.cout_reel and record.cout_reel < 0:
                raise ValidationError('Le coût réel doit être positif.')
    
    @api.constrains('duree_estimee', 'main_oeuvre_requise')
    def _check_durees_positives(self):
        """Vérifie que les durées sont positives"""
        for record in self:
            if record.duree_estimee and record.duree_estimee <= 0:
                raise ValidationError('La durée estimée doit être strictement positive.')
            if record.main_oeuvre_requise and record.main_oeuvre_requise <= 0:
                raise ValidationError('La main d\'œuvre requise doit être strictement positive.')

    # ONCHANGE
    @api.onchange('parcelle_id')
    def _onchange_parcelle(self):
        """Met à jour l'exploitation quand la parcelle change"""
        if self.parcelle_id:
            self.exploitation_id = self.parcelle_id.exploitation_id
    
    @api.onchange('culture_id')
    def _onchange_culture(self):
        """Met à jour la parcelle et l'exploitation quand la culture change"""
        if self.culture_id:
            self.parcelle_id = self.culture_id.parcelle_id
            self.exploitation_id = self.culture_id.exploitation_id
