# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)


class SmartAgriAIModel(models.Model):
    """Modèles d'Intelligence Artificielle pour l'agriculture"""
    
    _name = 'smart_agri_ai_model'
    _description = 'Modèle IA Agricole'
    _order = 'name'
    _rec_name = 'display_name'
    
    # IDENTIFICATION
    name = fields.Char('Nom du modèle', required=True)
    code = fields.Char('Code unique', required=True, size=20)
    description = fields.Text('Description du modèle')
    
    # TYPE DE MODÈLE
    type_modele = fields.Selection([
        ('prediction_rendement', 'Prédiction de rendement'),
        ('recommandation_culture', 'Recommandation de culture'),
        ('detection_stress', 'Détection de stress'),
        ('optimisation_ressources', 'Optimisation des ressources'),
        ('simulation_climatique', 'Simulation climatique'),
        ('analyse_spatiale', 'Analyse spatiale'),
        ('ensemble', 'Modèle ensemble')
    ], string='Type de modèle', required=True)
    
    # ALGORITHME ET TECHNOLOGIE
    algorithme = fields.Selection([
        ('random_forest', 'Random Forest'),
        ('xgboost', 'XGBoost'),
        ('neural_network', 'Réseau de neurones'),
        ('svm', 'Support Vector Machine'),
        ('linear_regression', 'Régression linéaire'),
        ('logistic_regression', 'Régression logistique'),
        ('decision_tree', 'Arbre de décision'),
        ('knn', 'K-Nearest Neighbors'),
        ('naive_bayes', 'Naive Bayes'),
        ('ensemble', 'Ensemble (Voting/Bagging)')
    ], string='Algorithme principal', required=True)
    
    # VERSION ET ÉVOLUTION
    version = fields.Char('Version', default='1.0.0')
    date_creation = fields.Date('Date de création', default=fields.Date.today, readonly=True)
    date_derniere_entrainement = fields.Date('Dernier entraînement')
    date_derniere_evaluation = fields.Date('Dernière évaluation')
    
    # PERFORMANCE ET MÉTRIQUES
    accuracy = fields.Float('Précision (%)', digits=(5, 2))
    precision = fields.Float('Précision (Precision)', digits=(5, 3))
    recall = fields.Float('Rappel (Recall)', digits=(5, 3))
    f1_score = fields.Float('Score F1', digits=(5, 3))
    mse = fields.Float('Erreur quadratique moyenne', digits=(8, 4))
    mae = fields.Float('Erreur absolue moyenne', digits=(8, 4))
    r2_score = fields.Float('Score R²', digits=(5, 3))
    
    # DONNÉES D'ENTRAÎNEMENT
    nb_echantillons_entrainement = fields.Integer('Échantillons d\'entraînement')
    nb_echantillons_test = fields.Integer('Échantillons de test')
    nb_features = fields.Integer('Nombre de features')
    nb_classes = fields.Integer('Nombre de classes (classification)')
    
    # PARAMÈTRES DU MODÈLE
    parametres = fields.Text('Paramètres du modèle (JSON)')
    hyperparametres = fields.Text('Hyperparamètres optimisés (JSON)')
    
    # FICHIERS ET ARTÉFACTS
    chemin_modele = fields.Char('Chemin du fichier modèle')
    chemin_scaler = fields.Char('Chemin du scaler')
    chemin_encoder = fields.Char('Chemin de l\'encodeur')
    
    # STATUT ET UTILISATION
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('training', 'En entraînement'),
        ('trained', 'Entraîné'),
        ('evaluating', 'En évaluation'),
        ('evaluated', 'Évalué'),
        ('deployed', 'Déployé'),
        ('archived', 'Archivé')
    ], string='État', default='draft', required=True)
    
    actif = fields.Boolean('Modèle actif', default=False)
    production = fields.Boolean('En production', default=False)
    
    # MÉTADONNÉES
    auteur = fields.Char('Auteur/Équipe')
    documentation = fields.Text('Documentation technique')
    limitations = fields.Text('Limitations connues')
    notes = fields.Text('Notes et observations')
    
    # RELATIONS
    # TEMPORAIREMENT COMMENTÉ POUR RÉSOLUDRE L'ERREUR DE CHARGEMENT
    # prediction_ids = fields.One2many('smart_agri_ai_prediction', 'modele_id', string='Prédictions')
    
    # CHAMPS CALCULÉS
    display_name = fields.Char('Nom affiché', compute='_compute_display_name', store=True)
    performance_globale = fields.Float('Performance globale', compute='_compute_performance_globale', store=True)
    
    @api.depends('name', 'version', 'algorithme')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.name} v{record.version} ({record.algorithme})"
    
    @api.depends('accuracy', 'precision', 'recall', 'f1_score', 'r2_score')
    def _compute_performance_globale(self):
        for record in self:
            scores = []
            if record.accuracy:
                scores.append(record.accuracy / 100)  # Normalisation 0-1
            if record.precision:
                scores.append(record.precision)
            if record.recall:
                scores.append(record.recall)
            if record.f1_score:
                scores.append(record.f1_score)
            if record.r2_score:
                scores.append(max(0, record.r2_score))  # R² peut être négatif
            
            if scores:
                record.performance_globale = sum(scores) / len(scores)
            else:
                record.performance_globale = 0.0
    
    # CONTRAINTES
    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.search_count([('code', '=', record.code), ('id', '!=', record.id)]) > 0:
                raise ValidationError('Le code du modèle doit être unique.')
    
    @api.constrains('accuracy', 'precision', 'recall', 'f1_score')
    def _check_metrics_range(self):
        for record in self:
            # Accuracy est en pourcentage (0-100)
            if record.accuracy and (record.accuracy < 0 or record.accuracy > 100):
                raise ValidationError('Le champ accuracy doit être compris entre 0 et 100.')
            
            # Les autres métriques sont en probabilité (0-1)
            for field in ['precision', 'recall', 'f1_score']:
                value = getattr(record, field)
                if value and (value < 0 or value > 1):
                    raise ValidationError(f'Le champ {field} doit être compris entre 0 et 1.')
    
    # MÉTHODES MÉTIER
    def action_entrainer_modele(self):
        """Lance l'entraînement du modèle IA"""
        self.ensure_one()
        
        if self.state not in ['draft', 'trained', 'evaluated']:
            raise ValidationError('Le modèle ne peut pas être entraîné dans son état actuel.')
        
        # Simulation d'entraînement
        self.write({
            'state': 'training',
            'date_derniere_entrainement': fields.Date.today()
        })
        
        # Génération de métriques de performance simulées
        self._simuler_entrainement()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Entraînement terminé',
                'message': f'Le modèle {self.name} a été entraîné avec succès.',
                'type': 'success',
            }
        }
    
    def _simuler_entrainement(self):
        """Simule l'entraînement et génère des métriques réalistes"""
        # Métriques selon le type de modèle
        if self.type_modele == 'prediction_rendement':
            self._generer_metriques_regression()
        elif self.type_modele == 'recommandation_culture':
            self._generer_metriques_classification()
        else:
            self._generer_metriques_mixtes()
        
        # Mise à jour du statut
        self.write({
            'state': 'trained',
            'nb_echantillons_entrainement': random.randint(5000, 50000),
            'nb_echantillons_test': random.randint(1000, 10000),
            'nb_features': random.randint(20, 100),
            'nb_classes': random.randint(3, 10) if self.type_modele == 'recommandation_culture' else 1
        })
    
    def _generer_metriques_regression(self):
        """Génère des métriques pour un modèle de régression"""
        self.write({
            'accuracy': 0.0,  # Pas d'accuracy pour la régression
            'precision': 0.0,  # Pas de precision pour la régression
            'recall': 0.0,     # Pas de recall pour la régression
            'f1_score': 0.0,   # Pas de F1 pour la régression
            'mse': round(random.uniform(0.01, 0.5), 4),
            'mae': round(random.uniform(0.05, 0.3), 4),
            'r2_score': round(random.uniform(0.7, 0.95), 3)
        })
    
    def _generer_metriques_classification(self):
        """Génère des métriques pour un modèle de classification"""
        self.write({
            'accuracy': round(random.uniform(75, 95), 2),  # Pourcentage (0-100)
            'precision': round(random.uniform(0.7, 0.9), 3),  # Probabilité (0-1)
            'recall': round(random.uniform(0.7, 0.9), 3),  # Probabilité (0-1)
            'f1_score': round(random.uniform(0.7, 0.9), 3),  # Probabilité (0-1)
            'mse': 0.0,        # Pas de MSE pour la classification
            'mae': 0.0,        # Pas de MAE pour la classification
            'r2_score': 0.0    # Pas de R² pour la classification
        })
    
    def _generer_metriques_mixtes(self):
        """Génère des métriques mixtes"""
        self.write({
            'accuracy': round(random.uniform(70, 90), 2),  # Pourcentage (0-100)
            'precision': round(random.uniform(0.6, 0.85), 3),  # Probabilité (0-1)
            'recall': round(random.uniform(0.6, 0.85), 3),  # Probabilité (0-1)
            'f1_score': round(random.uniform(0.6, 0.85), 3),  # Probabilité (0-1)
            'mse': round(random.uniform(0.02, 0.4), 4),
            'mae': round(random.uniform(0.08, 0.25), 4),
            'r2_score': round(random.uniform(0.6, 0.9), 3)
        })
    
    def action_evaluer_modele(self):
        """Lance l'évaluation du modèle IA"""
        self.ensure_one()
        
        if self.state != 'trained':
            raise ValidationError('Le modèle doit être entraîné avant d\'être évalué.')
        
        # Simulation d'évaluation
        self.write({
            'state': 'evaluating',
            'date_derniere_evaluation': fields.Date.today()
        })
        
        # Amélioration légère des métriques (réaliste)
        self._ameliorer_metriques_evaluation()
        
        # Mise à jour du statut
        self.write({'state': 'evaluated'})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Évaluation terminée',
                'message': f'Le modèle {self.name} a été évalué avec succès.',
                'type': 'success',
            }
        }
    
    def _ameliorer_metriques_evaluation(self):
        """Améliore légèrement les métriques après évaluation"""
        if self.accuracy:
            self.accuracy = min(100, self.accuracy + random.uniform(0.5, 2.0))
        if self.precision:
            self.precision = min(1.0, self.precision + random.uniform(0.01, 0.05))
        if self.recall:
            self.recall = min(1.0, self.recall + random.uniform(0.01, 0.05))
        if self.f1_score:
            self.f1_score = min(1.0, self.f1_score + random.uniform(0.01, 0.05))
        if self.r2_score:
            self.r2_score = min(1.0, self.r2_score + random.uniform(0.01, 0.03))
    
    def action_deployer_modele(self):
        """Déploie le modèle en production"""
        self.ensure_one()
        
        if self.state != 'evaluated':
            raise ValidationError('Le modèle doit être évalué avant d\'être déployé.')
        
        self.write({
            'state': 'deployed',
            'actif': True,
            'production': True
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Déploiement réussi',
                'message': f'Le modèle {self.name} est maintenant en production.',
                'type': 'success',
            }
        }
    
    def action_archiver_modele(self):
        """Archive le modèle"""
        self.ensure_one()
        
        self.write({
            'state': 'archived',
            'actif': False,
            'production': False
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Modèle archivé',
                'message': f'Le modèle {self.name} a été archivé.',
                'type': 'info',
            }
        }
    
    # MÉTHODES D'ANALYSE
    @api.model
    def get_modeles_actifs(self, type_modele=None):
        """Récupère les modèles actifs selon le type"""
        domain = [('actif', '=', True), ('state', '=', 'deployed')]
        if type_modele:
            domain.append(('type_modele', '=', type_modele))
        
        return self.search(domain, order='performance_globale desc')
    
    @api.model
    def get_statistiques_modeles(self):
        """Calcule les statistiques globales des modèles"""
        modeles = self.search([])
        
        stats = {
            'total': len(modeles),
            'actifs': len(modeles.filtered(lambda m: m.actif)),
            'production': len(modeles.filtered(lambda m: m.production)),
            'par_type': {},
            'par_algorithme': {},
            'performance_moyenne': 0.0
        }
        
        # Statistiques par type
        for type_modele in self._fields['type_modele'].selection:
            type_code = type_modele[0]
            modeles_type = modeles.filtered(lambda m: m.type_modele == type_code)
            stats['par_type'][type_code] = len(modeles_type)
        
        # Statistiques par algorithme
        for algo in self._fields['algorithme'].selection:
            algo_code = algo[0]
            modeles_algo = modeles.filtered(lambda m: m.algorithme == algo_code)
            stats['par_algorithme'][algo_code] = len(modeles_algo)
        
        # Performance moyenne
        performances = [m.performance_globale for m in modeles if m.performance_globale > 0]
        if performances:
            stats['performance_moyenne'] = sum(performances) / len(performances)
        
        return stats
    
    def get_features_importance(self):
        """Récupère l'importance des features (simulée)"""
        if not self.nb_features:
            return {}
        
        features = [f'feature_{i}' for i in range(1, self.nb_features + 1)]
        importance = {}
        
        for feature in features:
            # Simulation d'importance des features
            if 'temperature' in feature.lower() or 'climat' in feature.lower():
                importance[feature] = round(random.uniform(0.8, 1.0), 3)
            elif 'sol' in feature.lower() or 'ph' in feature.lower():
                importance[feature] = round(random.uniform(0.6, 0.9), 3)
            elif 'eau' in feature.lower() or 'irrigation' in feature.lower():
                importance[feature] = round(random.uniform(0.5, 0.8), 3)
            else:
                importance[feature] = round(random.uniform(0.1, 0.6), 3)
        
        # Tri par importance décroissante
        return dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
