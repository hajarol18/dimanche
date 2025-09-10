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
    
    # ==================== LIENS AVEC LES DONNÉES RÉELLES ====================
    exploitation_id = fields.Many2one(
        'smart_agri_exploitation',
        string='Exploitation',
        required=True,
        help='Exploitation agricole pour cette simulation'
    )
    
    parcelle_id = fields.Many2one(
        'smart_agri_parcelle',
        string='Parcelle',
        domain="[('exploitation_id', '=', exploitation_id)]",
        help='Parcelle spécifique (optionnel)'
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
    
    # ==================== MÉTHODES DE MISE À JOUR AUTOMATIQUE ====================
    
    @api.onchange('scenario_rcp')
    def _onchange_scenario_rcp(self):
        """Met à jour automatiquement les paramètres climatiques selon le scénario RCP choisi"""
        if self.scenario_rcp:
            if self.scenario_rcp == 'rcp26':
                # RCP 2.6 - Optimiste (limitation à +1.5°C)
                self.augmentation_temperature = 1.5
                self.variation_precipitations = 0.0
                self.rayonnement_solaire = 550.0
                self.humidite_relative = 70.0
                self.frequence_evenements_extremes = 15.0
                self.amplitude_thermique = 12.0
                
            elif self.scenario_rcp == 'rcp45':
                # RCP 4.5 - Intermédiaire (+2.4°C en 2100)
                self.augmentation_temperature = 2.4
                self.variation_precipitations = -5.0
                self.rayonnement_solaire = 600.0
                self.humidite_relative = 65.0
                self.frequence_evenements_extremes = 25.0
                self.amplitude_thermique = 15.0
                
            elif self.scenario_rcp == 'rcp60':
                # RCP 6.0 - Intermédiaire-Haut (+2.8°C en 2100)
                self.augmentation_temperature = 2.8
                self.variation_precipitations = -10.0
                self.rayonnement_solaire = 650.0
                self.humidite_relative = 60.0
                self.frequence_evenements_extremes = 35.0
                self.amplitude_thermique = 18.0
                
            elif self.scenario_rcp == 'rcp85':
                # RCP 8.5 - Pessimiste (+4.8°C en 2100)
                self.augmentation_temperature = 4.8
                self.variation_precipitations = -20.0
                self.rayonnement_solaire = 750.0
                self.humidite_relative = 50.0
                self.frequence_evenements_extremes = 50.0
                self.amplitude_thermique = 22.0
    
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
        ('biennale', 'Biennale'),
        ('triennale', 'Triennale'),
        ('quadriennale', 'Quadriennale')
    ], string='Rotation des Cultures', default='triennale')
    
    couverture_sol = fields.Selection([
        ('aucune', 'Aucune'),
        ('paillage', 'Paillage'),
        ('engrais_vert', 'Engrais Vert'),
        ('culture_intercalaire', 'Culture Intercalaire')
    ], string='Couverture du Sol', default='aucune')
    
    adaptation_climatique = fields.Selection([
        ('aucune', 'Aucune'),
        ('varietes_resistantes', 'Variétés Résistantes'),
        ('irrigation_adaptee', 'Irrigation Adaptée'),
        ('ombrage', 'Ombrage'),
        ('serre', 'Serre')
    ], string='Adaptation Climatique', default='aucune')
    
    # ==================== RÉSULTATS DE LA SIMULATION ====================
    rendement_predit = fields.Float(
        string='Rendement Prédit',
        help='Rendement prédit en tonnes par hectare',
        readonly=True
    )
    
    score_ia = fields.Integer(
        string='Score IA',
        help='Score de confiance de l\'IA (0-100%)',
        readonly=True
    )
    
    niveau_risque = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé')
    ], string='Niveau de Risque', readonly=True)
    
    confiance = fields.Integer(
        string='Confiance',
        help='Niveau de confiance de la prédiction (0-100%)',
        readonly=True
    )
    
    # ==================== MÉTHODES DE SIMULATION ====================
    
    def action_lancer_simulation(self):
        """Lancer la simulation IA"""
        try:
            # Validation des paramètres
            self._valider_parametres()
            
            # Mise à jour de l'état
            self.state = 'simulation_en_cours'
            
            # Calcul des résultats
            resultats = self._calculer_resultats_simulation()
            
            # Mise à jour des champs de résultats
            self.write({
                'rendement_predit': resultats['rendement_predit'],
                'score_ia': resultats['score_ia'],
                'niveau_risque': resultats['niveau_risque'],
                'confiance': resultats['confiance'],
                'state': 'termine'
            })
            
            # Message de succès
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '✅ Simulation Terminée !',
                    'message': f'🎯 Rendement prédit : {resultats["rendement_predit"]} t/ha\n🤖 Score IA : {resultats["score_ia"]}%\n⚠️ Niveau de risque : {resultats["niveau_risque"]}\n💯 Confiance : {resultats["confiance"]}%\n\n💡 Vérifiez la section "Résultats" ci-dessous !',
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except ValidationError as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '❌ Erreur de Validation',
                    'message': str(e),
                    'type': 'danger',
                    'sticky': False,
                }
            }
        except Exception as e:
            _logger.error(f"Erreur lors de la simulation : {str(e)}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '❌ Erreur de Simulation',
                    'message': f'Une erreur est survenue : {str(e)}',
                    'type': 'danger',
                    'sticky': False,
                }
            }
    
    def action_sauvegarder_scenario(self):
        """Sauvegarder le scénario"""
        try:
            self._valider_parametres()
            self.state = 'brouillon'
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '💾 Scénario Sauvegardé',
                    'message': f'Le scénario "{self.name}" a été sauvegardé avec succès !',
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '❌ Erreur de Sauvegarde',
                    'message': f'Erreur lors de la sauvegarde : {str(e)}',
                    'type': 'danger',
                    'sticky': False,
                }
            }
    
    def action_comparer_scenarios(self):
        """Comparer les scénarios"""
        if self.state != 'termine':
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '⚠️ Simulation Non Terminée',
                    'message': 'Vous devez d\'abord lancer la simulation !',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '📊 Comparaison des Scénarios',
                'message': f'Comparaison pour {self.name}:\n• RCP {self.scenario_rcp}\n• Rendement : {self.rendement_predit} t/ha\n• Score IA : {self.score_ia}%\n• Risque : {self.niveau_risque}',
                'type': 'info',
                'sticky': False,
            }
        }
    
    def action_export_resultats(self):
        """Exporter les résultats"""
        if self.state != 'termine':
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '⚠️ Simulation Non Terminée',
                    'message': 'Vous devez d\'abord lancer la simulation !',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '📤 Export des Résultats',
                'message': f'Rapport exporté pour {self.name}:\n• Date : {self.date_creation.strftime("%d/%m/%Y")}\n• RCP : {self.scenario_rcp}\n• Rendement : {self.rendement_predit} t/ha\n• Score IA : {self.score_ia}%',
                'type': 'success',
                'sticky': False,
            }
        }
    
    # ==================== MÉTHODES PRIVÉES ====================
    
    def _valider_parametres(self):
        """Valider les paramètres de la simulation"""
        if not self.name:
            raise ValidationError("Le nom du scénario est obligatoire")
        
        if not self.exploitation_id:
            raise ValidationError("L'exploitation est obligatoire")
        
        if not self.type_culture:
            raise ValidationError("Le type de culture est obligatoire")
        
        if not self.stade_developpement:
            raise ValidationError("Le stade de développement est obligatoire")
        
        if not self.type_sol:
            raise ValidationError("Le type de sol est obligatoire")
    
    def _calculer_resultats_simulation(self):
        """Calculer les résultats de la simulation"""
        return {
            'rendement_predit': self._calculer_rendement_predit(),
            'score_ia': self._calculer_score_ia(),
            'niveau_risque': self._evaluer_niveau_risque(),
            'confiance': self._calculer_confiance(),
        }
    
    def _calculer_rendement_predit(self):
        """Calculer le rendement prédit"""
        # Rendement de base selon le type de culture
        rendements_base = {
            'cereales': 8.0,
            'legumineuses': 3.5,
            'arboriculture': 15.0,
            'maraichage': 25.0,
            'viticulture': 12.0,
            'elevage': 0.0
        }
        
        rendement_base = rendements_base.get(self.type_culture, 5.0)
        
        # Ajustements selon les paramètres climatiques
        ajustement_temp = 1.0 - (self.augmentation_temperature * 0.05)
        ajustement_precip = 1.0 + (self.variation_precipitations * 0.01)
        
        # Ajustements selon les paramètres agricoles
        ajustement_ph = 1.0
        if hasattr(self, 'ph_sol') and self.ph_sol:
            if 6.0 <= self.ph_sol <= 7.5:
                ajustement_ph = 1.1
            elif self.ph_sol < 5.5 or self.ph_sol > 8.5:
                ajustement_ph = 0.8
        
        ajustement_rayonnement = 1.0
        if hasattr(self, 'rayonnement_solaire') and self.rayonnement_solaire:
            if 500 <= self.rayonnement_solaire <= 700:
                ajustement_rayonnement = 1.1
            elif self.rayonnement_solaire > 800:
                ajustement_rayonnement = 0.9
        
        ajustement_humidite = 1.0
        if hasattr(self, 'humidite_relative') and self.humidite_relative:
            if 50 <= self.humidite_relative <= 80:
                ajustement_humidite = 1.05
            elif self.humidite_relative < 30 or self.humidite_relative > 90:
                ajustement_humidite = 0.85
        
        # Calcul du rendement final
        rendement_predit = rendement_base * ajustement_temp * ajustement_precip * ajustement_ph * ajustement_rayonnement * ajustement_humidite
        
        return round(max(0.5, rendement_predit), 2)  # Minimum 0.5 t/ha
    
    def _calculer_score_ia(self):
        """Calculer le score IA"""
        score = 70  # Score de base
        
        # Ajustements selon la qualité des données
        if self.exploitation_id and self.parcelle_id:
            score += 10
        if self.date_semis:
            score += 5
        if hasattr(self, 'ph_sol') and self.ph_sol:
            score += 5
        if self.type_culture and self.stade_developpement:
            score += 10
        
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
        confiance = 85  # Confiance de base
        
        # Ajustements selon la qualité des données
        if self.augmentation_temperature > 0:
            confiance -= 5
        if self.variation_precipitations < 0:
            confiance -= 5
        
        return max(confiance, 60)
