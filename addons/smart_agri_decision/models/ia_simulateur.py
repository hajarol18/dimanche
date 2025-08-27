# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class SmartAgriIASimulateur(models.Model):
    """Simulateur IA - Scénarios Agricoles et Climatiques"""
    
    _name = 'smart_agri_ia_simulateur'
    _description = 'Simulateur IA - Test de Scénarios Agricoles'
    _order = 'date_creation desc'
    
    # ==================== CHAMPS DE BASE ====================
    name = fields.Char(
        string='Nom du Scénario',
        required=True,
        help='Nom du scénario de simulation'
    )
    
    description = fields.Text(
        string='Description',
        help='Description détaillée du scénario'
    )
    
    state = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('simulation_en_cours', 'Simulation en Cours'),
        ('termine', 'Terminé'),
        ('valide', 'Validé')
    ], string='État', default='brouillon', required=True)
    
    date_creation = fields.Datetime(
        string='Date de Création',
        default=fields.Datetime.now,
        help='Date de création du scénario'
    )
    
    # ==================== PARAMÈTRES CLIMATIQUES ====================
    augmentation_temperature = fields.Float(
        string='Augmentation Température',
        help='Augmentation de température en °C',
        default=2.5
    )
    
    variation_precipitations = fields.Float(
        string='Variation Précipitations',
        help='Variation des précipitations en %',
        default=-10.0
    )
    
    vitesse_vent = fields.Float(
        string='Vitesse du Vent',
        help='Vitesse du vent en km/h',
        default=12.0
    )
    
    rayonnement_solaire = fields.Float(
        string='Rayonnement Solaire',
        help='Rayonnement solaire en W/m²',
        default=650.0
    )
    
    humidite_relative = fields.Float(
        string='Humidité Relative',
        help='Humidité relative en %',
        default=65.0
    )
    
    frequence_evenements_extremes = fields.Float(
        string='Fréquence Événements Extrêmes',
        help='Fréquence des événements extrêmes en %',
        default=25.0
    )
    
    amplitude_thermique = fields.Float(
        string='Amplitude Thermique',
        help='Amplitude thermique en °C',
        default=15.0
    )
    
    scenario_rcp = fields.Selection([
        ('rcp26', 'RCP 2.6 - Optimiste'),
        ('rcp45', 'RCP 4.5 - Intermédiaire'),
        ('rcp60', 'RCP 6.0 - Modéré'),
        ('rcp85', 'RCP 8.5 - Pessimiste')
    ], string='Scénario RCP', required=True, default='rcp45')
    
    # ==================== PARAMÈTRES AGRICOLES ====================
    type_culture = fields.Selection([
        ('cereales', 'Céréales'),
        ('legumineuses', 'Légumineuses'),
        ('arboriculture', 'Arboriculture'),
        ('maraichage', 'Maraîchage'),
        ('viticulture', 'Viticulture'),
        ('elevage', 'Élevage')
    ], string='Type de Culture', required=True)
    
    stade_developpement = fields.Selection([
        ('semis', 'Semis'),
        ('levée', 'Levée'),
        ('debut_vegetation', 'Début Végétation'),
        ('developpement', 'Développement'),
        ('floraison', 'Floraison'),
        ('fructification', 'Fructification'),
        ('maturite', 'Maturité'),
        ('recolte', 'Récolte')
    ], string='Stade de Développement', required=True)
    
    date_semis = fields.Date(
        string='Date de Semis',
        help='Date de semis de la culture'
    )
    
    type_sol = fields.Selection([
        ('argileux', 'Argileux'),
        ('limoneux', 'Limoneux'),
        ('sableux', 'Sableux'),
        ('calcaire', 'Calcaire'),
        ('humique', 'Humique')
    ], string='Type de Sol', required=True)
    
    ph_sol = fields.Float(
        string='pH du Sol',
        help='pH du sol (0-14)',
        default=7.0
    )
    
    capacite_retention = fields.Float(
        string='Capacité de Rétention',
        help='Capacité de rétention en mm',
        default=150.0
    )
    
    densite_plantation = fields.Float(
        string='Densité de Plantation',
        help='Densité de plantation en plants/ha',
        default=50000.0
    )
    
    systeme_irrigation = fields.Selection([
        ('pluviale', 'Pluviale'),
        ('gravitaire', 'Gravitaire'),
        ('aspersion', 'Aspersion'),
        ('goutte_goutte', 'Goutte-à-goutte'),
        ('pivot', 'Pivot'),
        ('rampe', 'Rampe')
    ], string='Système d\'Irrigation')
    
    # ==================== PARAMÈTRES DE GESTION ====================
    frequence_irrigation = fields.Integer(
        string='Fréquence Irrigation',
        help='Fréquence d\'irrigation en jours',
        default=7
    )
    
    dose_irrigation = fields.Float(
        string='Dose Irrigation',
        help='Dose d\'irrigation en mm',
        default=25.0
    )
    
    frequence_fertilisation = fields.Integer(
        string='Fréquence Fertilisation',
        help='Fréquence de fertilisation en jours',
        default=30
    )
    
    dose_engrais = fields.Float(
        string='Dose Engrais',
        help='Dose d\'engrais en kg/ha',
        default=100.0
    )
    
    protection_phytosanitaire = fields.Selection([
        ('aucune', 'Aucune'),
        ('preventive', 'Préventive'),
        ('curative', 'Curative'),
        ('integrée', 'Intégrée')
    ], string='Protection Phytosanitaire', default='preventive')
    
    rotation_cultures = fields.Selection([
        ('aucune', 'Aucune'),
        ('bienale', 'Bienale'),
        ('triennale', 'Triennale'),
        ('quadriennale', 'Quadriennale')
    ], string='Rotation des Cultures', default='triennale')
    
    couverture_sol = fields.Selection([
        ('aucune', 'Aucune'),
        ('engrais_vert', 'Engrais Vert'),
        ('paillage', 'Paillage'),
        ('mulch', 'Mulch')
    ], string='Couverture du Sol', default='aucune')
    
    adaptation_climatique = fields.Selection([
        ('aucune', 'Aucune'),
        ('varietes_resistantes', 'Variétés Résistantes'),
        ('modification_calendrier', 'Modification Calendrier'),
        ('changement_cultures', 'Changement Cultures')
    ], string='Adaptation Climatique', default='aucune')
    
    # ==================== RÉSULTATS DE LA SIMULATION ====================
    rendement_predit = fields.Float(
        string='Rendement Prédit',
        help='Rendement prédit par l\'IA en t/ha'
    )
    
    score_ia = fields.Integer(
        string='Score IA',
        help='Score de confiance de l\'IA (0-100%)'
    )
    
    niveau_risque = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé')
    ], string='Niveau de Risque')
    
    confiance = fields.Integer(
        string='Confiance',
        help='Niveau de confiance de la prédiction (0-100%)'
    )
    
    resultat_principal = fields.Text(
        string='Résultat Principal',
        help='Résultat principal de la simulation'
    )
    
    resultat_detaille = fields.Text(
        string='Résultat Détaillé',
        help='Résultat détaillé de la simulation'
    )
    
    recommandations = fields.Text(
        string='Recommandations',
        help='Recommandations de l\'IA'
    )
    
    actions_prioritaires = fields.Text(
        string='Actions Prioritaires',
        help='Actions prioritaires recommandées'
    )
    
    # ==================== SCÉNARIOS COMPARATIFS ====================
    scenario_optimiste = fields.Text(
        string='Scénario Optimiste',
        help='Résultats du scénario optimiste'
    )
    
    scenario_realiste = fields.Text(
        string='Scénario Réaliste',
        help='Résultats du scénario réaliste'
    )
    
    scenario_pessimiste = fields.Text(
        string='Scénario Pessimiste',
        help='Résultats du scénario pessimiste'
    )
    
    # ==================== OPTIMISATIONS RECOMMANDÉES ====================
    # Note: This relation is commented out until the related model is created
    # optimisations_recommandees_ids = fields.One2many(
    #     'smart_agri_optimisation_ia',
    #     'simulateur_id',
    #     string='Optimisations Recommandées',
    #     help='Optimisations recommandées par l\'IA'
    # )
    
    # ==================== GRAPHIQUES COMPARATIFS ====================
    graphique_comparaison_scenarios = fields.Binary(
        string='Graphique Comparaison Scénarios',
        help='Graphique de comparaison des scénarios'
    )
    
    graphique_impact_climatique = fields.Binary(
        string='Graphique Impact Climatique',
        help='Graphique d\'impact climatique'
    )
    
    # ==================== RELATIONS ====================
    exploitation_id = fields.Many2one(
        'smart_agri_exploitation',
        string='Exploitation',
        help='Exploitation concernée par la simulation'
    )
    
    parcelle_id = fields.Many2one(
        'smart_agri_parcelle',
        string='Parcelle',
        help='Parcelle concernée par la simulation'
    )
    
    # ==================== MÉTHODES ====================
    @api.model
    def create(self, vals):
        """Création avec initialisation automatique"""
        if not vals.get('name'):
            vals['name'] = f"Simulation IA - {fields.Datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Initialisation des paramètres par défaut selon le scénario RCP
        if vals.get('scenario_rcp'):
            vals.update(self._get_parametres_rcp(vals['scenario_rcp']))
        
        return super().create(vals)
    
    def action_lancer_simulation(self):
        """Lancer la simulation IA"""
        self.ensure_one()
        
        # Validation des paramètres
        self._valider_parametres()
        
        # Changement d'état
        self.state = 'simulation_en_cours'
        
        # Exécution de la simulation
        resultats = self._executer_simulation_complete()
        
        # Mise à jour des résultats
        self._mettre_a_jour_resultats(resultats)
        
        # Changement d'état final
        self.state = 'termine'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Simulation Terminée'),
                'message': _('La simulation IA a été exécutée avec succès !'),
                'type': 'success',
                'sticky': False,
            }
        }
    
    def action_sauvegarder_scenario(self):
        """Sauvegarder le scénario"""
        self.ensure_one()
        
        # Validation et sauvegarde
        self._valider_parametres()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Scénario Sauvegardé'),
                'message': _('Le scénario a été sauvegardé avec succès !'),
                'type': 'success',
                'sticky': False,
            }
        }
    
    def action_comparer_scenarios(self):
        """Comparer différents scénarios"""
        self.ensure_one()
        
        # Logique de comparaison
        comparaison = self._generer_comparaison_scenarios()
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Comparaison Scénarios'),
            'res_model': 'smart_agri_comparaison_scenarios',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_simulateur_id': self.id,
                'default_comparaison_html': comparaison,
            }
        }
    
    def action_export_resultats(self):
        """Exporter les résultats"""
        self.ensure_one()
        
        # Génération du rapport d'export
        rapport = self._generer_rapport_export()
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Export Résultats'),
            'res_model': 'smart_agri_export_simulation',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_simulateur_id': self.id,
                'default_contenu_export': rapport,
            }
        }
    
    def action_lancer_simulation_complete(self):
        """Lancer la simulation IA complète"""
        return self.action_lancer_simulation()
    
    # ==================== MÉTHODES PRIVÉES ====================
    def _get_parametres_rcp(self, scenario_rcp):
        """Obtenir les paramètres par défaut selon le scénario RCP"""
        parametres = {
            'rcp26': {
                'augmentation_temperature': 1.5,
                'variation_precipitations': 5.0,
                'frequence_evenements_extremes': 15.0,
            },
            'rcp45': {
                'augmentation_temperature': 2.5,
                'variation_precipitations': -10.0,
                'frequence_evenements_extremes': 25.0,
            },
            'rcp60': {
                'augmentation_temperature': 3.5,
                'variation_precipitations': -15.0,
                'frequence_evenements_extremes': 35.0,
            },
            'rcp85': {
                'augmentation_temperature': 4.8,
                'variation_precipitations': -25.0,
                'frequence_evenements_extremes': 50.0,
            }
        }
        
        return parametres.get(scenario_rcp, {})
    
    def _valider_parametres(self):
        """Valider les paramètres de simulation"""
        if self.augmentation_temperature < -10 or self.augmentation_temperature > 10:
            raise ValidationError(_('L\'augmentation de température doit être entre -10°C et +10°C'))
        
        if self.variation_precipitations < -50 or self.variation_precipitations > 50:
            raise ValidationError(_('La variation des précipitations doit être entre -50% et +50%'))
        
        if self.ph_sol < 0 or self.ph_sol > 14:
            raise ValidationError(_('Le pH du sol doit être entre 0 et 14'))
    
    def _executer_simulation_complete(self):
        """Exécuter la simulation IA complète"""
        # Logique de simulation IA
        resultats = {
            'rendement_predit': self._calculer_rendement_predit(),
            'score_ia': self._calculer_score_ia(),
            'niveau_risque': self._evaluer_niveau_risque(),
            'confiance': self._calculer_confiance(),
            'resultat_principal': self._generer_resultat_principal(),
            'resultat_detaille': self._generer_resultat_detaille(),
            'recommandations': self._generer_recommandations(),
            'actions_prioritaires': self._generer_actions_prioritaires(),
            'scenarios': self._generer_scenarios_comparatifs(),
        }
        
        return resultats
    
    def _mettre_a_jour_resultats(self, resultats):
        """Mettre à jour les résultats de la simulation"""
        self.write({
            'rendement_predit': resultats['rendement_predit'],
            'score_ia': resultats['score_ia'],
            'niveau_risque': resultats['niveau_risque'],
            'confiance': resultats['confiance'],
            'resultat_principal': resultats['resultat_principal'],
            'resultat_detaille': resultats['resultat_detaille'],
            'recommandations': resultats['recommandations'],
            'actions_prioritaires': resultats['actions_prioritaires'],
            'scenario_optimiste': resultats['scenarios']['optimiste'],
            'scenario_realiste': resultats['scenarios']['realiste'],
            'scenario_pessimiste': resultats['scenarios']['pessimiste'],
        })
    
    def _calculer_rendement_predit(self):
        """Calculer le rendement prédit"""
        # Logique de calcul basée sur les paramètres
        rendement_base = 4.0  # t/ha
        
        # Ajustements selon les paramètres
        ajustement_temp = 1 + (self.augmentation_temperature * 0.1)
        ajustement_precip = 1 + (self.variation_precipitations * 0.01)
        ajustement_ph = 1 + ((self.ph_sol - 7.0) * 0.05)
        
        rendement_predit = rendement_base * ajustement_temp * ajustement_precip * ajustement_ph
        
        return round(rendement_predit, 2)
    
    def _calculer_score_ia(self):
        """Calculer le score IA"""
        # Logique de calcul du score
        score = 80  # Score de base
        
        # Ajustements selon la qualité des données
        if self.exploitation_id and self.parcelle_id:
            score += 10
        if self.date_semis:
            score += 5
        if self.ph_sol > 0:
            score += 5
        
        return min(score, 100)
    
    def _evaluer_niveau_risque(self):
        """Évaluer le niveau de risque"""
        if self.augmentation_temperature > 3 or self.variation_precipitations < -20:
            return 'eleve'
        elif self.augmentation_temperature > 2 or self.variation_precipitations < -10:
            return 'modere'
        else:
            return 'faible'
    
    def _calculer_confiance(self):
        """Calculer le niveau de confiance"""
        # Logique de calcul de la confiance
        confiance = 85  # Confiance de base
        
        # Ajustements selon la qualité des données
        if self.augmentation_temperature > 0:
            confiance -= 5
        if self.variation_precipitations < 0:
            confiance -= 5
        
        return max(confiance, 60)
    
    def _generer_resultat_principal(self):
        """Générer le résultat principal"""
        return f"Rendement prédit : {self.rendement_predit} t/ha avec un niveau de risque {self.niveau_risque}"
    
    def _generer_resultat_detaille(self):
        """Générer le résultat détaillé"""
        return f"""
        Simulation basée sur le scénario {self.scenario_rcp}.
        Augmentation température : +{self.augmentation_temperature}°C
        Variation précipitations : {self.variation_precipitations}%
        Type de culture : {self.type_culture}
        Stade : {self.stade_developpement}
        """
    
    def _generer_recommandations(self):
        """Générer les recommandations"""
        recommandations = []
        
        if self.augmentation_temperature > 2:
            recommandations.append("Prévoir une irrigation supplémentaire")
        
        if self.variation_precipitations < -15:
            recommandations.append("Installer un système d'irrigation")
        
        if self.ph_sol < 6.5:
            recommandations.append("Apporter des amendements calcaires")
        
        return "\n".join(recommandations) if recommandations else "Aucune recommandation spéciale"
    
    def _generer_actions_prioritaires(self):
        """Générer les actions prioritaires"""
        actions = []
        
        if self.niveau_risque == 'eleve':
            actions.append("1. Réviser le calendrier cultural")
            actions.append("2. Préparer des mesures d'urgence")
            actions.append("3. Surveiller les conditions météo")
        elif self.niveau_risque == 'modere':
            actions.append("1. Ajuster l'irrigation")
            actions.append("2. Surveiller le développement")
        else:
            actions.append("1. Continuer les pratiques actuelles")
        
        return "\n".join(actions)
    
    def _generer_scenarios_comparatifs(self):
        """Générer les scénarios comparatifs"""
        return {
            'optimiste': f"Rendement optimal : {self.rendement_predit * 1.2:.2f} t/ha avec conditions parfaites",
            'realiste': f"Rendement attendu : {self.rendement_predit:.2f} t/ha avec gestion optimale",
            'pessimiste': f"Rendement minimal : {self.rendement_predit * 0.8:.2f} t/ha en cas de conditions défavorables"
        }
    
    def _generer_comparaison_scenarios(self):
        """Générer la comparaison des scénarios"""
        return f"""
        <h3>Comparaison des Scénarios - {self.name}</h3>
        <p><strong>Scénario actuel :</strong> {self.scenario_rcp}</p>
        <p><strong>Rendement prédit :</strong> {self.rendement_predit} t/ha</p>
        <p><strong>Niveau de risque :</strong> {self.niveau_risque}</p>
        <p><strong>Confiance IA :</strong> {self.confiance}%</p>
        """
    
    def _generer_rapport_export(self):
        """Générer le rapport d'export"""
        return f"""
        <h2>Rapport de Simulation IA - {self.name}</h2>
        <p><strong>Date :</strong> {self.date_creation.strftime('%Y-%m-%d %H:%M')}</p>
        <p><strong>Scénario RCP :</strong> {self.scenario_rcp}</p>
        <p><strong>Rendement prédit :</strong> {self.rendement_predit} t/ha</p>
        <p><strong>Score IA :</strong> {self.score_ia}%</p>
        <p><strong>Niveau de risque :</strong> {self.niveau_risque}</p>
        <p><strong>Confiance :</strong> {self.confiance}%</p>
        """
