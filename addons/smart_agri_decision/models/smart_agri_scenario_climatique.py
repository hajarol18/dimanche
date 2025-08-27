# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class SmartAgriScenarioClimatique(models.Model):
    """Scénarios climatiques IPCC RCP pour simulation agricole"""

    _name = 'smart_agri_scenario_climatique'
    _description = 'Scénario Climatique IPCC RCP'
    _order = 'name'

    # IDENTIFICATION
    name = fields.Char('Nom du scénario', required=True)
    code_scenario = fields.Char('Code RCP', required=True, help='Code IPCC RCP (ex: RCP 4.5, RCP 8.5)')
    description = fields.Text('Description du scénario')
    
    # CARACTÉRISTIQUES CLIMATIQUES
    type_scenario = fields.Selection([
        ('rcp26', 'RCP 2.6 - Optimiste'),
        ('rcp45', 'RCP 4.5 - Intermédiaire'),
        ('rcp60', 'RCP 6.0 - Intermédiaire-Haut'),
        ('rcp85', 'RCP 8.5 - Pessimiste')
    ], string='Type de scénario', required=True)
    
    periode_debut = fields.Date('Période de début', default=fields.Date.today)
    periode_fin = fields.Date('Période de fin', default=lambda self: fields.Date.today() + timedelta(days=365))
    
    # PARAMÈTRES CLIMATIQUES
    augmentation_temperature = fields.Float('Augmentation température (°C)', help='Augmentation moyenne de température')
    variation_precipitation = fields.Float('Variation précipitations (%)', help='Variation des précipitations')
    frequence_secheresse = fields.Float('Fréquence sécheresse (%)', help='Fréquence des épisodes de sécheresse')
    intensite_events = fields.Float('Intensité événements extrêmes', help='Intensité des événements climatiques extrêmes')
    
    # IMPACTS AGRICOLES PRÉDITS
    impact_rendement = fields.Selection([
        ('fortement_negatif', 'Fortement négatif'),
        ('negatif', 'Négatif'),
        ('neutre', 'Neutre'),
        ('positif', 'Positif'),
        ('fortement_positif', 'Fortement positif')
    ], string='Impact sur rendement', compute='_compute_impact_agricole', store=True)
    
    impact_irrigation = fields.Selection([
        ('fortement_negatif', 'Fortement négatif'),
        ('negatif', 'Négatif'),
        ('neutre', 'Neutre'),
        ('positif', 'Positif'),
        ('fortement_positif', 'Fortement positif')
    ], string='Impact sur irrigation', compute='_compute_impact_agricole', store=True)
    
    impact_risques = fields.Selection([
        ('fortement_negatif', 'Fortement négatif'),
        ('negatif', 'Négatif'),
        ('neutre', 'Neutre'),
        ('positif', 'Positif'),
        ('fortement_positif', 'Fortement positif')
    ], string='Impact sur risques', compute='_compute_impact_agricole', store=True)
    
    # RÉSULTATS DE SIMULATION
    resultat_simulation = fields.Text('Résultats de simulation', readonly=True)
    recommandations = fields.Text('Recommandations agricoles', readonly=True)
    mesures_adaptation = fields.Text('Mesures d\'adaptation', readonly=True)
    
    # RELATIONS
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True)
    meteo_ids = fields.One2many('smart_agri_meteo', 'scenario_id', string='Données météo simulées')
    
    # STATUT
    state = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('simule', 'Simulé'),
        ('valide', 'Validé'),
        ('archive', 'Archivé')
    ], string='État', default='brouillon')
    
    active = fields.Boolean('Actif', default=True)
    
    @api.depends('augmentation_temperature', 'variation_precipitation', 'frequence_secheresse', 'intensite_events')
    def _compute_impact_agricole(self):
        """Calcule automatiquement l'impact agricole basé sur les paramètres climatiques"""
        for record in self:
            # Logique de calcul d'impact basée sur les paramètres
            score = 0
            
            # Impact de la température
            if record.augmentation_temperature <= 1.5:
                score += 2  # Positif
            elif record.augmentation_temperature <= 2.5:
                score += 1  # Légèrement positif
            elif record.augmentation_temperature <= 3.5:
                score += 0  # Neutre
            elif record.augmentation_temperature <= 4.5:
                score -= 1  # Négatif
            else:
                score -= 2  # Fortement négatif
            
            # Impact des précipitations
            if record.variation_precipitation >= 10:
                score += 1  # Positif
            elif record.variation_precipitation >= -5:
                score += 0  # Neutre
            elif record.variation_precipitation >= -15:
                score -= 1  # Négatif
            else:
                score -= 2  # Fortement négatif
            
            # Impact des sécheresses
            if record.frequence_secheresse <= 5:
                score += 1  # Positif
            elif record.frequence_secheresse <= 15:
                score += 0  # Neutre
            elif record.frequence_secheresse <= 25:
                score -= 1  # Négatif
            else:
                score -= 2  # Fortement négatif
            
            # Déterminer l'impact global
            if score >= 3:
                impact = 'fortement_positif'
            elif score >= 1:
                impact = 'positif'
            elif score >= -1:
                impact = 'neutre'
            elif score >= -3:
                impact = 'negatif'
            else:
                impact = 'fortement_negatif'
            
            record.impact_rendement = impact
            record.impact_irrigation = impact
            record.impact_risques = impact
    
    def action_simuler_scenario(self):
        """Simule le scénario climatique et génère les résultats"""
        self.ensure_one()
        
        try:
            # Simulation des impacts climatiques
            resultats = self._simuler_impacts_climatiques()
            
            # Mise à jour des résultats
            self.write({
                'resultat_simulation': resultats['simulation'],
                'recommandations': resultats['recommandations'],
                'mesures_adaptation': resultats['mesures'],
                'state': 'simule'
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Simulation terminée',
                    'message': f'Scénario {self.name} simulé avec succès. Consultez les résultats.',
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            _logger.error(f"Erreur lors de la simulation: {str(e)}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Erreur de simulation',
                    'message': f'Erreur lors de la simulation: {str(e)}',
                    'type': 'danger',
                    'sticky': False,
                }
            }
    
    def _simuler_impacts_climatiques(self):
        """Simule les impacts climatiques du scénario"""
        # Simulation sophistiquée basée sur les paramètres
        temp_impact = self.augmentation_temperature
        precip_impact = self.variation_precipitation
        secheresse_impact = self.frequence_secheresse
        
        # Génération des résultats de simulation
        simulation = f"""
        SIMULATION CLIMATIQUE - {self.name}
        
        PARAMÈTRES CLIMATIQUES:
        • Augmentation température: +{temp_impact}°C
        • Variation précipitations: {precip_impact}%
        • Fréquence sécheresse: {secheresse_impact}%
        
        IMPACTS PRÉDITS:
        • Rendement agricole: {self.impact_rendement.replace('_', ' ').title()}
        • Besoins en irrigation: {self.impact_irrigation.replace('_', ' ').title()}
        • Risques climatiques: {self.impact_risques.replace('_', ' ').title()}
        
        PÉRIODE: {self.periode_debut} à {self.periode_fin}
        """
        
        # Génération des recommandations
        recommandations = self._generer_recommandations()
        
        # Génération des mesures d'adaptation
        mesures = self._generer_mesures_adaptation()
        
        return {
            'simulation': simulation,
            'recommandations': recommandations,
            'mesures': mesures
        }
    
    def _generer_recommandations(self):
        """Génère des recommandations agricoles basées sur le scénario"""
        if self.type_scenario == 'rcp26':
            return """
            RECOMMANDATIONS POUR RCP 2.6 (OPTIMISTE):
            • Maintenir les pratiques agricoles actuelles
            • Surveillance modérée des tendances climatiques
            • Adaptation progressive des variétés
            • Optimisation de l'irrigation existante
            """
        elif self.type_scenario == 'rcp45':
            return """
            RECOMMANDATIONS POUR RCP 4.5 (INTERMÉDIAIRE):
            • Adapter les dates de semis
            • Introduire des variétés plus résistantes
            • Améliorer les systèmes d'irrigation
            • Diversifier les cultures
            """
        elif self.type_scenario == 'rcp60':
            return """
            RECOMMANDATIONS POUR RCP 6.0 (INTERMÉDIAIRE-HAUT):
            • Révolutionner les pratiques culturales
            • Systèmes d'irrigation intelligents
            • Cultures résistantes au stress
            • Planification à long terme
            """
        else:  # RCP 8.5
            return """
            RECOMMANDATIONS POUR RCP 8.5 (PESSIMISTE):
            • Transformation complète des systèmes agricoles
            • Technologies d'adaptation avancées
            • Cultures ultra-résistantes
            • Stratégies de survie agricole
            """
    
    def _generer_mesures_adaptation(self):
        """Génère des mesures d'adaptation spécifiques"""
        if self.impact_rendement == 'fortement_negatif':
            return """
            MESURES D'ADAPTATION URGENTES:
            • Installation de systèmes d'irrigation
            • Choix de variétés ultra-résistantes
            • Protection contre les événements extrêmes
            • Planification de replantation
            """
        elif self.impact_rendement == 'negatif':
            return """
            MESURES D'ADAPTATION RECOMMANDÉES:
            • Amélioration des systèmes d'irrigation
            • Choix de variétés résistantes
            • Surveillance accrue des cultures
            • Planification préventive
            """
        elif self.impact_rendement == 'neutre':
            return """
            MESURES D'ADAPTATION MODÉRÉES:
            • Surveillance des tendances
            • Optimisation des pratiques existantes
            • Préparation aux variations
            """
        else:
            return """
            MESURES D'ADAPTATION POSITIVES:
            • Exploitation des opportunités
            • Optimisation des rendements
            • Planification d'expansion
            """
