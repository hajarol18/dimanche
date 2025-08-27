# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class SmartAgriIADetectionStress(models.Model):
    """Détection Automatique de Stress IA - SmartAgriDecision"""
    
    _name = 'smart_agri_ia_detection_stress'
    _description = 'Détection IA - Stress Climatique et Hydrique'
    _order = 'date_detection desc'
    
    # ==================== CHAMPS DE BASE ====================
    name = fields.Char(
        string='Nom de la Détection',
        required=True,
        help='Nom de la détection de stress'
    )
    
    description = fields.Text(
        string='Description',
        help='Description de la détection de stress'
    )
    
    state = fields.Selection([
        ('surveillance', 'Surveillance'),
        ('detection', 'Détection'),
        ('alerte', 'Alerte'),
        ('correction', 'Correction'),
        ('resolu', 'Résolu')
    ], string='État', default='surveillance', required=True)
    
    # ==================== RELATIONS ====================
    exploitation_id = fields.Many2one(
        'smart_agri_exploitation',
        string='Exploitation',
        required=True,
        help='Exploitation concernée'
    )
    
    parcelle_id = fields.Many2one(
        'smart_agri_parcelle',
        string='Parcelle',
        help='Parcelle concernée'
    )
    
    # ==================== DÉTECTION AUTOMATIQUE IA ====================
    type_stress = fields.Selection([
        ('aucun', 'Aucun'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé')
    ], string='Type de Stress Détecté', default='aucun', required=True)
    
    niveau_stress = fields.Integer(
        string='Niveau de Stress',
        default=0,
        help='Niveau de stress sur une échelle de 0 à 100'
    )
    
    confiance_detection = fields.Integer(
        string='Confiance IA',
        default=0,
        help='Niveau de confiance de la détection IA (0-100%)'
    )
    
    date_detection = fields.Datetime(
        string='Dernière Détection',
        default=fields.Datetime.now,
        help='Date et heure de la dernière détection'
    )
    
    description_stress = fields.Text(
        string='Description du Stress',
        help='Description détaillée du stress détecté'
    )
    
    # ==================== PARAMÈTRES CLIMATIQUES ANALYSÉS ====================
    temperature_actuelle = fields.Float(
        string='Température Actuelle',
        help='Température actuelle en °C'
    )
    
    temperature_seuil = fields.Float(
        string='Température Seuil',
        help='Température seuil critique en °C'
    )
    
    ecart_temperature = fields.Float(
        string='Écart Température',
        help='Écart par rapport à la température normale en °C'
    )
    
    statut_temperature = fields.Selection([
        ('normal', 'Normal'),
        ('attention', 'Attention'),
        ('critique', 'Critique')
    ], string='Statut Température', default='normal')
    
    humidite_sol = fields.Float(
        string='Humidité Sol',
        help='Humidité du sol en %'
    )
    
    humidite_seuil = fields.Float(
        string='Humidité Seuil',
        help='Humidité seuil critique en %'
    )
    
    deficit_hydrique = fields.Float(
        string='Déficit Hydrique',
        help='Déficit hydrique en %'
    )
    
    statut_hydrique = fields.Selection([
        ('optimal', 'Optimal'),
        ('faible', 'Faible'),
        ('critique', 'Critique')
    ], string='Statut Hydrique', default='optimal')
    
    precipitations = fields.Float(
        string='Précipitations',
        help='Précipitations actuelles en mm'
    )
    
    precipitations_normales = fields.Float(
        string='Précipitations Normales',
        help='Précipitations normales pour la période en mm'
    )
    
    deficit_precipitations = fields.Float(
        string='Déficit Précipitations',
        help='Déficit en précipitations en mm'
    )
    
    statut_precipitations = fields.Selection([
        ('suffisant', 'Suffisant'),
        ('insuffisant', 'Insuffisant'),
        ('deficitaire', 'Déficitaire')
    ], string='Statut Précipitations', default='suffisant')
    
    # ==================== ANALYSE DES CULTURES ====================
    culture_affectee = fields.Char(
        string='Culture Affectée',
        help='Culture affectée par le stress'
    )
    
    stade_developpement = fields.Selection([
        ('semis', 'Semis'),
        ('levée', 'Levée'),
        ('debut_vegetation', 'Début Végétation'),
        ('developpement', 'Développement'),
        ('floraison', 'Floraison'),
        ('fructification', 'Fructification'),
        ('maturite', 'Maturité'),
        ('recolte', 'Récolte')
    ], string='Stade de Développement')
    
    impact_rendement = fields.Float(
        string='Impact sur Rendement',
        help='Impact estimé sur le rendement en %'
    )
    
    duree_exposition = fields.Float(
        string='Durée d\'Exposition',
        help='Durée d\'exposition au stress en heures'
    )
    
    symptomes_visibles = fields.Text(
        string='Symptômes Visibles',
        help='Symptômes visibles du stress sur la culture'
    )
    
    resistance_culture = fields.Selection([
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('elevee', 'Élevée')
    ], string='Résistance de la Culture', default='moyenne')
    
    # ==================== ALERTES INTELLIGENTES ====================
    # Note: These relations are commented out until the related models are created
    # alertes_ia_ids = fields.One2many(
    #     'smart_agri_alerte_ia',
    #     'detection_stress_id',
    #     string='Alertes IA',
    #     help='Alertes intelligentes générées par l\'IA'
    # )
    # 
    # ==================== ACTIONS CORRECTIVES AUTOMATIQUES ====================
    # actions_correctives_ids = fields.One2many(
    #     'smart_agri_action_corrective',
    #     'detection_stress_id',
    #     string='Actions Correctives',
    #     help='Actions correctives automatiques recommandées'
    # )
    
    # ==================== SURVEILLANCE CONTINUE ====================
    frequence_surveillance = fields.Selection([
        ('continue', 'Continue'),
        ('quotidienne', 'Quotidienne'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuelle', 'Mensuelle')
    ], string='Fréquence Surveillance', default='quotidienne')
    
    prochaine_analyse = fields.Datetime(
        string='Prochaine Analyse',
        help='Date et heure de la prochaine analyse'
    )
    
    nombre_analyses = fields.Integer(
        string='Nombre d\'Analyses',
        default=0,
        help='Nombre d\'analyses effectuées'
    )
    
    tendance_stress = fields.Selection([
        ('diminue', 'Diminue'),
        ('stable', 'Stable'),
        ('augmente', 'Augmente')
    ], string='Tendance Stress', default='stable')
    
    notes_surveillance = fields.Text(
        string='Notes de Surveillance',
        help='Notes et observations de surveillance'
    )
    
    # ==================== GRAPHIQUES D'ÉVOLUTION ====================
    graphique_evolution_stress = fields.Binary(
        string='Graphique Évolution Stress',
        help='Graphique d\'évolution du stress dans le temps'
    )
    
    graphique_repartition_stress = fields.Binary(
        string='Graphique Répartition Stress',
        help='Graphique de répartition des types de stress'
    )
    
    # ==================== MÉTHODES ====================
    @api.model
    def create(self, vals):
        """Création avec initialisation automatique"""
        if not vals.get('name'):
            vals['name'] = f"Détection Stress - {fields.Datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Initialisation de la surveillance
        vals['prochaine_analyse'] = fields.Datetime.now() + timedelta(days=1)
        
        return super().create(vals)
    
    def action_analyser_stress(self):
        """Analyser le stress avec l'IA"""
        self.ensure_one()
        
        # Changement d'état
        self.state = 'detection'
        
        # Analyse automatique IA
        resultats_analyse = self._analyser_stress_ia()
        
        # Mise à jour des résultats
        self._mettre_a_jour_analyse(resultats_analyse)
        
        # Génération des alertes
        self._generer_alertes_automatiques()
        
        # Planification de la prochaine analyse
        self._planifier_prochaine_analyse()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Analyse Terminée'),
                'message': _('L\'analyse IA du stress a été effectuée avec succès !'),
                'type': 'success',
                'sticky': False,
            }
        }
    
    def action_generer_alertes(self):
        """Générer des alertes automatiques"""
        self.ensure_one()
        
        # Génération des alertes
        alertes_generees = self._generer_alertes_automatiques()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Alertes Générées'),
                'message': f'{len(alertes_generees)} nouvelles alertes ont été générées.',
                'type': 'info',
                'sticky': False,
            }
        }
    
    def action_appliquer_corrections(self):
        """Appliquer les corrections automatiques"""
        self.ensure_one()
        
        # Changement d'état
        self.state = 'correction'
        
        # Application des corrections
        corrections_appliquees = self._appliquer_corrections_automatiques()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Corrections Appliquées'),
                'message': f'{len(corrections_appliquees)} corrections ont été appliquées automatiquement.',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def action_planifier_surveillance(self):
        """Planifier la surveillance continue"""
        self.ensure_one()
        
        # Planification de la surveillance
        self._planifier_surveillance_continue()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Surveillance Planifiée'),
                'message': _('La surveillance continue a été planifiée avec succès !'),
                'type': 'success',
                'sticky': False,
            }
        }
    
    # ==================== MÉTHODES PRIVÉES ====================
    def _analyser_stress_ia(self):
        """Analyser le stress avec l'IA"""
        # Récupération des données actuelles
        donnees_actuelles = self._recuperer_donnees_actuelles()
        
        # Analyse IA des paramètres
        analyse_temperature = self._analyser_temperature(donnees_actuelles)
        analyse_hydrique = self._analyser_hydrique(donnees_actuelles)
        analyse_precipitations = self._analyser_precipitations(donnees_actuelles)
        
        # Évaluation globale du stress
        niveau_stress = self._evaluer_niveau_stress_global(
            analyse_temperature, analyse_hydrique, analyse_precipitations
        )
        
        # Analyse de l'impact sur les cultures
        impact_culture = self._analyser_impact_culture(donnees_actuelles, niveau_stress)
        
        return {
            'niveau_stress': niveau_stress,
            'type_stress': self._determiner_type_stress(niveau_stress),
            'confiance': self._calculer_confiance_detection(),
            'analyse_temperature': analyse_temperature,
            'analyse_hydrique': analyse_hydrique,
            'analyse_precipitations': analyse_precipitations,
            'impact_culture': impact_culture,
        }
    
    def _recuperer_donnees_actuelles(self):
        """Récupérer les données actuelles"""
        # Simulation de récupération de données
        return {
            'temperature': 28.5,
            'humidite_sol': 45.0,
            'precipitations': 5.0,
            'precipitations_normales': 25.0,
        }
    
    def _analyser_temperature(self, donnees):
        """Analyser les paramètres de température"""
        temperature = donnees.get('temperature', 20.0)
        seuil_critique = 30.0
        seuil_attention = 25.0
        
        ecart = temperature - 20.0  # Température normale
        
        if temperature > seuil_critique:
            statut = 'critique'
        elif temperature > seuil_attention:
            statut = 'attention'
        else:
            statut = 'normal'
        
        return {
            'actuelle': temperature,
            'seuil': seuil_critique,
            'ecart': ecart,
            'statut': statut,
        }
    
    def _analyser_hydrique(self, donnees):
        """Analyser les paramètres hydriques"""
        humidite = donnees.get('humidite_sol', 60.0)
        seuil_critique = 30.0
        seuil_attention = 45.0
        
        deficit = 100 - humidite
        
        if humidite < seuil_critique:
            statut = 'critique'
        elif humidite < seuil_attention:
            statut = 'faible'
        else:
            statut = 'optimal'
        
        return {
            'actuelle': humidite,
            'seuil': seuil_critique,
            'deficit': deficit,
            'statut': statut,
        }
    
    def _analyser_precipitations(self, donnees):
        """Analyser les paramètres de précipitations"""
        precip_actuelles = donnees.get('precipitations', 0.0)
        precip_normales = donnees.get('precipitations_normales', 25.0)
        
        deficit = precip_normales - precip_actuelles
        
        if deficit > 20:
            statut = 'deficitaire'
        elif deficit > 10:
            statut = 'insuffisant'
        else:
            statut = 'suffisant'
        
        return {
            'actuelles': precip_actuelles,
            'normales': precip_normales,
            'deficit': deficit,
            'statut': statut,
        }
    
    def _evaluer_niveau_stress_global(self, analyse_temp, analyse_hyd, analyse_precip):
        """Évaluer le niveau de stress global"""
        score_stress = 0
        
        # Contribution de la température
        if analyse_temp['statut'] == 'critique':
            score_stress += 40
        elif analyse_temp['statut'] == 'attention':
            score_stress += 20
        
        # Contribution de l'hydrique
        if analyse_hyd['statut'] == 'critique':
            score_stress += 35
        elif analyse_hyd['statut'] == 'faible':
            score_stress += 15
        
        # Contribution des précipitations
        if analyse_precip['statut'] == 'deficitaire':
            score_stress += 25
        elif analyse_precip['statut'] == 'insuffisant':
            score_stress += 10
        
        return min(score_stress, 100)
    
    def _determiner_type_stress(self, niveau_stress):
        """Déterminer le type de stress"""
        if niveau_stress >= 70:
            return 'eleve'
        elif niveau_stress >= 30:
            return 'modere'
        else:
            return 'aucun'
    
    def _calculer_confiance_detection(self):
        """Calculer la confiance de la détection"""
        # Logique de calcul de la confiance
        confiance = 85  # Confiance de base
        
        # Ajustements selon la qualité des données
        if self.exploitation_id and self.parcelle_id:
            confiance += 10
        if self.culture_affectee:
            confiance += 5
        
        return min(confiance, 100)
    
    def _analyser_impact_culture(self, donnees, niveau_stress):
        """Analyser l'impact sur la culture"""
        impact_rendement = 0
        
        if niveau_stress >= 70:
            impact_rendement = 25.0
        elif niveau_stress >= 30:
            impact_rendement = 10.0
        
        return {
            'impact_rendement': impact_rendement,
            'duree_exposition': 24.0,  # heures
            'symptomes': self._generer_symptomes(niveau_stress),
            'resistance': 'moyenne',
        }
    
    def _generer_symptomes(self, niveau_stress):
        """Générer les symptômes selon le niveau de stress"""
        if niveau_stress >= 70:
            return "Flétrissement sévère, décoloration des feuilles, arrêt de croissance"
        elif niveau_stress >= 30:
            return "Flétrissement modéré, ralentissement de croissance"
        else:
            return "Aucun symptôme visible"
    
    def _mettre_a_jour_analyse(self, resultats):
        """Mettre à jour les résultats de l'analyse"""
        self.write({
            'niveau_stress': resultats['niveau_stress'],
            'type_stress': resultats['type_stress'],
            'confiance_detection': resultats['confiance'],
            'date_detection': fields.Datetime.now(),
            'temperature_actuelle': resultats['analyse_temperature']['actuelle'],
            'temperature_seuil': resultats['analyse_temperature']['seuil'],
            'ecart_temperature': resultats['analyse_temperature']['ecart'],
            'statut_temperature': resultats['analyse_temperature']['statut'],
            'humidite_sol': resultats['analyse_hydrique']['actuelle'],
            'humidite_seuil': resultats['analyse_hydrique']['seuil'],
            'deficit_hydrique': resultats['analyse_hydrique']['deficit'],
            'statut_hydrique': resultats['analyse_hydrique']['statut'],
            'precipitations': resultats['analyse_precipitations']['actuelles'],
            'precipitations_normales': resultats['analyse_precipitations']['normales'],
            'deficit_precipitations': resultats['analyse_precipitations']['deficit'],
            'statut_precipitations': resultats['analyse_precipitations']['statut'],
            'impact_rendement': resultats['impact_culture']['impact_rendement'],
            'duree_exposition': resultats['impact_culture']['duree_exposition'],
            'symptomes_visibles': resultats['impact_culture']['symptomes'],
            'resistance_culture': resultats['impact_culture']['resistance'],
            'description_stress': self._generer_description_stress(resultats),
        })
    
    def _generer_description_stress(self, resultats):
        """Générer la description du stress"""
        return f"""
        Stress détecté de niveau {resultats['niveau_stress']}/100.
        Type : {resultats['type_stress']}
        Impact sur rendement estimé : {resultats['impact_culture']['impact_rendement']}%
        Confiance IA : {resultats['confiance']}%
        """
    
    def _generer_alertes_automatiques(self):
        """Générer des alertes automatiques"""
        alertes = []
        
        if self.niveau_stress >= 70:
            alertes.append({
                'type_alerte': 'danger',
                'titre': 'Stress Critique Détecté',
                'description': 'Niveau de stress critique nécessitant une action immédiate',
                'niveau_urgence': 'eleve',
                'actions_recommandees': 'Irrigation d\'urgence, ombrage, surveillance renforcée',
                'delai_action': 'Immédiat',
            })
        elif self.niveau_stress >= 30:
            alertes.append({
                'type_alerte': 'warning',
                'titre': 'Stress Modéré Détecté',
                'description': 'Niveau de stress modéré nécessitant une surveillance',
                'niveau_urgence': 'modere',
                'actions_recommandees': 'Ajuster l\'irrigation, surveiller l\'évolution',
                'delai_action': '24h',
            })
        
        # Création des alertes
        for alerte_data in alertes:
            self.env['smart_agri_alerte_ia'].create({
                'detection_stress_id': self.id,
                **alerte_data
            })
        
        return alertes
    
    def _appliquer_corrections_automatiques(self):
        """Appliquer les corrections automatiques"""
        corrections = []
        
        if self.statut_hydrique == 'critique':
            corrections.append({
                'type_action': 'irrigation_urgence',
                'description': 'Irrigation d\'urgence pour compenser le déficit hydrique',
                'parametres': 'Dose: 50mm, Durée: 2h',
                'priorite': 'elevee',
                'cout_estime': 150.0,
                'efficacite_attendue': 'Élevée',
            })
        
        if self.statut_temperature == 'critique':
            corrections.append({
                'type_action': 'ombrage_urgence',
                'description': 'Installation d\'ombrage pour réduire le stress thermique',
                'parametres': 'Filet ombrage 70%, Surface: 100%',
                'priorite': 'elevee',
                'cout_estime': 200.0,
                'efficacite_attendue': 'Élevée',
            })
        
        # Création des actions correctives
        for correction_data in corrections:
            self.env['smart_agri_action_corrective'].create({
                'detection_stress_id': self.id,
                **correction_data
            })
        
        return corrections
    
    def _planifier_prochaine_analyse(self):
        """Planifier la prochaine analyse"""
        if self.frequence_surveillance == 'continue':
            self.prochaine_analyse = fields.Datetime.now() + timedelta(hours=1)
        elif self.frequence_surveillance == 'quotidienne':
            self.prochaine_analyse = fields.Datetime.now() + timedelta(days=1)
        elif self.frequence_surveillance == 'hebdomadaire':
            self.prochaine_analyse = fields.Datetime.now() + timedelta(weeks=1)
        elif self.frequence_surveillance == 'mensuelle':
            self.prochaine_analyse = fields.Datetime.now() + timedelta(days=30)
    
    def _planifier_surveillance_continue(self):
        """Planifier la surveillance continue"""
        # Mise à jour de la fréquence
        if self.niveau_stress >= 70:
            self.frequence_surveillance = 'continue'
        elif self.niveau_stress >= 30:
            self.frequence_surveillance = 'quotidienne'
        else:
            self.frequence_surveillance = 'hebdomadaire'
        
        # Planification de la prochaine analyse
        self._planifier_prochaine_analyse()
        
        # Mise à jour des notes
        self.notes_surveillance = f"""
        Surveillance planifiée le {fields.Datetime.now().strftime('%Y-%m-%d %H:%M')}
        Fréquence : {self.frequence_surveillance}
        Prochaine analyse : {self.prochaine_analyse.strftime('%Y-%m-%d %H:%M')}
        """
