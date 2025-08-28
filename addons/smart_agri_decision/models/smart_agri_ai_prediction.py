# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)


class SmartAgriAIPrediction(models.Model):
    """Prédictions et recommandations de l'IA agricole"""
    
    _name = 'smart_agri_ai_prediction'
    _description = 'Prédiction IA Agricole'
    _order = 'date_creation desc'
    _rec_name = 'display_name'
    
    # IDENTIFICATION
    name = fields.Char('Nom de la prédiction', required=True)
    code = fields.Char('Code unique', size=20)
    
    # RELATIONS
    modele_id = fields.Many2one('smart_agri_ai_model', string='Modèle IA', required=True, ondelete='cascade')
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle', required=True, ondelete='cascade')
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', related='parcelle_id.exploitation_id', store=True)
    culture_id = fields.Many2one('smart_agri_culture', string='Culture concernée')
    
    # TYPE DE PRÉDICTION
    type_prediction = fields.Selection([
        ('rendement', 'Prédiction de rendement'),
        ('culture_optimale', 'Culture optimale recommandée'),
        ('stress_detecte', 'Stress détecté'),
        ('optimisation_irrigation', 'Optimisation irrigation'),
        ('optimisation_engrais', 'Optimisation engrais'),
        ('risque_climatique', 'Risque climatique'),
        ('date_semis_optimale', 'Date de semis optimale'),
        ('date_recolte_optimale', 'Date de récolte optimale'),
        ('besoin_eau', 'Besoin en eau'),
        ('maladie_potentielle', 'Maladie potentielle')
    ], string='Type de prédiction', required=True)
    
    # DONNÉES D'ENTRÉE
    donnees_entree = fields.Text('Données d\'entrée (JSON)')
    features_utilisees = fields.Text('Features utilisées (JSON)')
    
    # RÉSULTATS DE LA PRÉDICTION
    prediction_brute = fields.Float('Prédiction brute')
    prediction_formatee = fields.Char('Prédiction formatée')
    classe_predite = fields.Char('Classe prédite')
    probabilite = fields.Float('Probabilité/Confiance (%)', digits=(5, 2))
    
    # INTERVALLES DE CONFIANCE
    intervalle_confiance_min = fields.Float('Intervalle confiance min')
    intervalle_confiance_max = fields.Float('Intervalle confiance max')
    marge_erreur = fields.Float('Marge d\'erreur')
    
    # RECOMMANDATIONS
    recommandation_principale = fields.Text('Recommandation principale')
    recommandations_secondaires = fields.Text('Recommandations secondaires')
    actions_immediates = fields.Text('Actions immédiates')
    actions_long_terme = fields.Text('Actions long terme')
    
    # MÉTRIQUES DE QUALITÉ
    score_confiance = fields.Float('Score de confiance', digits=(4, 3))
    qualite_donnees = fields.Selection([
        ('excellente', 'Excellente'),
        ('bonne', 'Bonne'),
        ('moyenne', 'Moyenne'),
        ('faible', 'Faible'),
        ('insuffisante', 'Insuffisante')
    ], string='Qualité des données d\'entrée', default='bonne')
    
    # CONTEXTE TEMPOREL
    date_creation = fields.Datetime('Date de création', default=fields.Datetime.now, readonly=True)
    date_prediction = fields.Date('Date de la prédiction')
    validite_jusqu_a = fields.Date('Valide jusqu\'à')
    frequence_mise_a_jour = fields.Selection([
        ('quotidienne', 'Quotidienne'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuelle', 'Mensuelle'),
        ('saisonniere', 'Saisonnière'),
        ('annuelle', 'Annuelle'),
        ('ponctuelle', 'Ponctuelle')
    ], string='Fréquence de mise à jour', default='quotidienne')
    
    # VALIDATION ET FEEDBACK
    validee = fields.Boolean('Prédiction validée')
    date_validation = fields.Date('Date de validation')
    utilisateur_validation = fields.Many2one('res.users', string='Utilisateur validation')
    feedback_utilisateur = fields.Selection([
        ('excellent', 'Excellent'),
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('mauvais', 'Mauvais'),
        ('tres_mauvais', 'Très mauvais')
    ], string='Feedback utilisateur')
    commentaire_validation = fields.Text('Commentaire de validation')
    
    # STATUT ET PRIORITÉ
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('generated', 'Générée'),
        ('validated', 'Validée'),
        ('applied', 'Appliquée'),
        ('expired', 'Expirée'),
        ('archived', 'Archivée')
    ], string='État', default='generated', required=True)
    
    priorite = fields.Selection([
        ('critique', 'Critique'),
        ('haute', 'Haute'),
        ('normale', 'Normale'),
        ('basse', 'Basse'),
        ('information', 'Information')
    ], string='Priorité', default='normale')
    
    # ALERTES ET NOTIFICATIONS
    alerte_active = fields.Boolean('Alerte active')
    niveau_alerte = fields.Selection([
        ('info', 'Information'),
        ('warning', 'Avertissement'),
        ('danger', 'Danger'),
        ('critical', 'Critique')
    ], string='Niveau d\'alerte', default='info')
    
    # MÉTADONNÉES
    source_donnees = fields.Text('Source des données utilisées')
    version_modele = fields.Char('Version du modèle utilisée')
    temps_execution = fields.Float('Temps d\'exécution (secondes)', digits=(6, 3))
    ressources_utilisees = fields.Text('Ressources utilisées (JSON)')
    
    # NOTES ET OBSERVATIONS
    notes = fields.Text('Notes et observations')
    
    # CHAMPS CALCULÉS
    display_name = fields.Char('Nom affiché', compute='_compute_display_name', store=True)
    age_prediction = fields.Integer('Âge de la prédiction (jours)', compute='_compute_age_prediction', store=True)
    urgence = fields.Selection([
        ('immediate', 'Immédiate'),
        ('urgente', 'Urgente'),
        ('normale', 'Normale'),
        ('faible', 'Faible')
    ], string='Urgence', compute='_compute_urgence', store=True)
    
    @api.depends('name', 'type_prediction', 'parcelle_id.name')
    def _compute_display_name(self):
        for record in self:
            if record.parcelle_id and record.type_prediction:
                record.display_name = f"{record.type_prediction.replace('_', ' ').title()} - {record.parcelle_id.name}"
            else:
                record.display_name = record.name or "Nouvelle prédiction"
    
    @api.depends('date_creation')
    def _compute_age_prediction(self):
        for record in self:
            if record.date_creation:
                delta = fields.Datetime.now() - record.date_creation
                record.age_prediction = delta.days
            else:
                record.age_prediction = 0
    
    @api.depends('priorite', 'niveau_alerte', 'age_prediction', 'validite_jusqu_a')
    def _compute_urgence(self):
        for record in self:
            urgence_score = 0
            
            # Score selon la priorité
            if record.priorite == 'critique':
                urgence_score += 4
            elif record.priorite == 'haute':
                urgence_score += 3
            elif record.priorite == 'normale':
                urgence_score += 2
            elif record.priorite == 'basse':
                urgence_score += 1
            
            # Score selon le niveau d'alerte
            if record.niveau_alerte == 'critical':
                urgence_score += 4
            elif record.niveau_alerte == 'danger':
                urgence_score += 3
            elif record.niveau_alerte == 'warning':
                urgence_score += 2
            elif record.niveau_alerte == 'info':
                urgence_score += 1
            
            # Score selon l'âge et la validité
            if record.validite_jusqu_a and record.validite_jusqu_a < fields.Date.today():
                urgence_score += 3
            elif record.age_prediction > 7:
                urgence_score += 2
            elif record.age_prediction > 3:
                urgence_score += 1
            
            # Détermination de l'urgence
            if urgence_score >= 7:
                record.urgence = 'immediate'
            elif urgence_score >= 5:
                record.urgence = 'urgente'
            elif urgence_score >= 3:
                record.urgence = 'normale'
            else:
                record.urgence = 'faible'
    
    # CONTRAINTES
    @api.constrains('probabilite')
    def _check_probabilite_range(self):
        for record in self:
            if record.probabilite and (record.probabilite < 0 or record.probabilite > 100):
                raise ValidationError('La probabilité doit être comprise entre 0 et 100%.')
    
    @api.constrains('date_prediction', 'validite_jusqu_a')
    def _check_dates_validite(self):
        for record in self:
            if record.date_prediction and record.validite_jusqu_a:
                if record.date_prediction > record.validite_jusqu_a:
                    raise ValidationError('La date de prédiction ne peut pas être postérieure à la date de validité.')
    
    # MÉTHODES MÉTIER
    def action_valider_prediction(self):
        """Valide la prédiction IA"""
        self.ensure_one()
        
        if self.state != 'generated':
            raise ValidationError('Seules les prédictions générées peuvent être validées.')
        
        self.write({
            'validee': True,
            'date_validation': fields.Date.today(),
            'utilisateur_validation': self.env.user.id,
            'state': 'validated'
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Prédiction validée',
                'message': f'La prédiction "{self.name}" a été validée avec succès.',
                'type': 'success',
            }
        }
    
    def action_appliquer_prediction(self):
        """Marque la prédiction comme appliquée"""
        self.ensure_one()
        
        if self.state != 'validated':
            raise ValidationError('Seules les prédictions validées peuvent être appliquées.')
        
        self.write({'state': 'applied'})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Prédiction appliquée',
                'message': f'La prédiction "{self.name}" a été marquée comme appliquée.',
                'type': 'success',
            }
        }
    
    def action_archiver_prediction(self):
        """Archive la prédiction"""
        self.ensure_one()
        
        self.write({'state': 'archived'})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Prédiction archivée',
                'message': f'La prédiction "{self.name}" a été archivée.',
                'type': 'info',
            }
        }
    
    def action_generer_recommandations(self):
        """Génère des recommandations basées sur la prédiction"""
        self.ensure_one()
        
        if self.type_prediction == 'rendement':
            self._generer_recommandations_rendement()
        elif self.type_prediction == 'culture_optimale':
            self._generer_recommandations_culture()
        elif self.type_prediction == 'stress_detecte':
            self._generer_recommandations_stress()
        else:
            self._generer_recommandations_generiques()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Recommandations générées',
                'message': f'Les recommandations pour "{self.name}" ont été générées.',
                'type': 'success',
            }
        }
    
    def _generer_recommandations_rendement(self):
        """Génère des recommandations pour optimiser le rendement"""
        rendement_predit = self.prediction_brute or 0
        
        if rendement_predit < 3.0:  # Rendement faible
            self.recommandation_principale = "Rendement prédit faible. Optimisation urgente recommandée."
            self.actions_immediates = "• Vérifier l'irrigation et la fertilisation\n• Analyser la qualité du sol\n• Contrôler les maladies et ravageurs"
            self.actions_long_terme = "• Améliorer la structure du sol\n• Planifier la rotation des cultures\n• Investir dans l'irrigation de précision"
        elif rendement_predit < 5.0:  # Rendement moyen
            self.recommandation_principale = "Rendement prédit moyen. Amélioration possible."
            self.actions_immediates = "• Optimiser l'apport en eau\n• Ajuster la fertilisation\n• Surveiller la croissance"
            self.actions_long_terme = "• Améliorer les pratiques culturales\n• Optimiser la densité de plantation"
        else:  # Rendement élevé
            self.recommandation_principale = "Rendement prédit élevé. Maintenir les bonnes pratiques."
            self.actions_immediates = "• Continuer les pratiques actuelles\n• Surveiller les signes de stress"
            self.actions_long_terme = "• Documenter les bonnes pratiques\n• Planifier la diversification"
    
    def _generer_recommandations_culture(self):
        """Génère des recommandations pour la culture optimale"""
        culture_recommandee = self.classe_predite or "Culture non spécifiée"
        
        self.recommandation_principale = f"Culture recommandée : {culture_recommandee}"
        self.actions_immediates = "• Préparer le sol selon les besoins de la culture\n• Planifier les semis\n• Vérifier la disponibilité des semences"
        self.actions_long_terme = "• Planifier la rotation des cultures\n• Évaluer la rentabilité\n• Considérer les marchés"
    
    def _generer_recommandations_stress(self):
        """Génère des recommandations pour gérer le stress"""
        type_stress = self.classe_predite or "Stress non spécifié"
        
        self.recommandation_principale = f"Stress détecté : {type_stress}"
        self.actions_immediates = "• Évaluer la gravité du stress\n• Appliquer les traitements appropriés\n• Surveiller l'évolution"
        self.actions_long_terme = "• Identifier les causes racines\n• Mettre en place des mesures préventives\n• Améliorer la résilience des cultures"
    
    def _generer_recommandations_generiques(self):
        """Génère des recommandations génériques"""
        self.recommandation_principale = "Analyse IA complétée. Suivre les recommandations spécifiques."
        self.actions_immediates = "• Analyser les résultats détaillés\n• Consulter les experts si nécessaire\n• Planifier les actions prioritaires"
        self.actions_long_terme = "• Intégrer les apprentissages\n• Améliorer les processus décisionnels"
    
    # MÉTHODES D'ANALYSE
    @api.model
    def get_predictions_urgentes(self, limite=10):
        """Récupère les prédictions urgentes"""
        domain = [
            ('state', 'in', ['generated', 'validated']),
            ('urgence', 'in', ['immediate', 'urgente']),
            ('active', '=', True)
        ]
        
        return self.search(domain, limit=limite, order='urgence desc, priorite desc')
    
    @api.model
    def get_statistiques_predictions(self, parcelle_id=None, date_debut=None, date_fin=None):
        """Calcule les statistiques des prédictions"""
        domain = [('active', '=', True)]
        
        if parcelle_id:
            domain.append(('parcelle_id', '=', parcelle_id))
        if date_debut:
            domain.append(('date_creation', '>=', date_debut))
        if date_fin:
            domain.append(('date_creation', '<=', date_fin))
        
        predictions = self.search(domain)
        
        stats = {
            'total': len(predictions),
            'validees': len(predictions.filtered(lambda p: p.validee)),
            'appliquees': len(predictions.filtered(lambda p: p.state == 'applied')),
            'par_type': {},
            'par_urgence': {},
            'precision_moyenne': 0.0,
            'confiance_moyenne': 0.0
        }
        
        # Statistiques par type
        for type_pred in self._fields['type_prediction'].selection:
            type_code = type_pred[0]
            preds_type = predictions.filtered(lambda p: p.type_prediction == type_code)
            stats['par_type'][type_code] = len(preds_type)
        
        # Statistiques par urgence
        for urgence in self._fields['urgence'].selection:
            urgence_code = urgence[0]
            preds_urgence = predictions.filtered(lambda p: p.urgence == urgence_code)
            stats['par_urgence'][urgence_code] = len(preds_urgence)
        
        # Métriques moyennes
        confiances = [p.probabilite for p in predictions if p.probabilite]
        if confiances:
            stats['confiance_moyenne'] = sum(confiances) / len(confiances)
        
        return stats
    
    def get_historique_predictions(self, parcelle_id, type_prediction=None, limite=50):
        """Récupère l'historique des prédictions pour une parcelle"""
        domain = [
            ('parcelle_id', '=', parcelle_id),
            ('state', '!=', 'archived')
        ]
        
        if type_prediction:
            domain.append(('type_prediction', '=', type_prediction))
        
        return self.search(domain, limit=limite, order='date_creation desc')
