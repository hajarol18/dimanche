# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class SmartAgriIAPredictions(models.Model):
    """Prédictions IA sophistiquées pour l'agriculture intelligente"""

    _name = 'smart_agri_ia_predictions'
    _description = 'Prédictions IA Agricoles Avancées'
    _order = 'date_creation desc'

    # ========================================
    # CHAMPS D'IDENTIFICATION
    # ========================================
    name = fields.Char('Nom de la prédiction', required=True)
    code = fields.Char('Code unique', required=True, copy=False)
    description = fields.Text('Description détaillée')
    date_creation = fields.Datetime('Date de création', default=fields.Datetime.now)
    date_execution = fields.Datetime('Date d\'exécution')
    
    # ========================================
    # RELATIONS PRINCIPALES
    # ========================================
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True)
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle')
    culture_id = fields.Many2one('smart_agri_culture', string='Culture')
    scenario_climatique_id = fields.Many2one('smart_agri_scenario_climatique', string='Scénario climatique')
    
    # ========================================
    # TYPE DE PRÉDICTION IA
    # ========================================
    type_prediction = fields.Selection([
        ('rendement', 'Prédiction de rendement'),
        ('culture_optimale', 'Culture optimale recommandée'),
        ('risque_climatique', 'Évaluation des risques climatiques'),
        ('irrigation', 'Optimisation de l\'irrigation'),
        ('engrais', 'Optimisation des engrais'),
        ('semis', 'Date optimale de semis'),
        ('recolte', 'Date optimale de récolte'),
        ('maladie', 'Prédiction des maladies'),
        ('stress_hydrique', 'Stress hydrique'),
        ('rotation_culturelle', 'Plan de rotation culturelle')
    ], string='Type de prédiction', required=True)
    
    # ========================================
    # DONNÉES D'ENTRÉE POUR L'IA
    # ========================================
    donnees_meteo = fields.Text('Données météorologiques')
    donnees_sol = fields.Text('Données pédologiques')
    donnees_culture = fields.Text('Données culturales')
    donnees_historiques = fields.Text('Données historiques')
    
    # Paramètres météorologiques
    temperature_moyenne = fields.Float('Température moyenne (°C)')
    precipitation_totale = fields.Float('Précipitations totales (mm)')
    humidite_moyenne = fields.Float('Humidité moyenne (%)')
    vitesse_vent = fields.Float('Vitesse du vent (km/h)')
    
    # Paramètres pédologiques
    ph_sol = fields.Float('pH du sol')
    azote_sol = fields.Float('Azote disponible (kg/ha)')
    phosphore_sol = fields.Float('Phosphore disponible (kg/ha)')
    potassium_sol = fields.Float('Potassium disponible (kg/ha)')
    capacite_retention = fields.Float('Capacité de rétention (mm)')
    
    # Paramètres culturaux
    stade_culture = fields.Selection([
        ('germination', 'Germination'),
        ('levée', 'Levée'),
        ('tallage', 'Tallage'),
        ('montaison', 'Montaison'),
        ('floraison', 'Floraison'),
        ('maturation', 'Maturation'),
        ('recolte', 'Récolte')
    ], string='Stade de développement')
    
    # ========================================
    # RÉSULTATS DE L'IA
    # ========================================
    resultat_principal = fields.Text('Résultat principal de l\'IA')
    resultat_detaille = fields.Text('Résultats détaillés')
    recommandations = fields.Text('Recommandations IA')
    actions_prioritaires = fields.Text('Actions prioritaires')
    
    # Métriques de performance
    confiance = fields.Float('Niveau de confiance (%)', default=0.0)
    precision = fields.Float('Précision (%)', default=0.0)
    score_ia = fields.Float('Score IA global', default=0.0)
    
    # Résultats spécifiques par type
    rendement_predit = fields.Float('Rendement prédit (t/ha)')
    rendement_optimal = fields.Float('Rendement optimal possible (t/ha)')
    gain_potentiel = fields.Float('Gain potentiel (%)')
    
    valeur_predite = fields.Float('Valeur prédite', help='Valeur principale prédite par l\'IA')
    
    # Risques et alertes
    niveau_risque = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('critique', 'Critique')
    ], string='Niveau de risque')
    
    type_risque = fields.Selection([
        ('secheresse', 'Sécheresse'),
        ('exces_eau', 'Excès d\'eau'),
        ('gel', 'Gel'),
        ('canicule', 'Canicule'),
        ('maladie', 'Maladie'),
        ('ravageur', 'Ravageur'),
        ('stress_nutritionnel', 'Stress nutritionnel')
    ], string='Type de risque principal')
    
    # ========================================
    # OPTIMISATION DES RESSOURCES
    # ========================================
    eau_optimale = fields.Float('Besoins en eau optimaux (m³/ha)')
    engrais_azote = fields.Float('Engrais azoté recommandé (kg/ha)')
    engrais_phosphore = fields.Float('Engrais phosphoré recommandé (kg/ha)')
    engrais_potassium = fields.Float('Engrais potassique recommandé (kg/ha)')
    main_oeuvre_estimee = fields.Float('Main d\'œuvre estimée (h/ha)')
    
    # ========================================
    # SCÉNARIOS ET SIMULATIONS
    # ========================================
    scenario_optimiste = fields.Text('Scénario optimiste')
    scenario_pessimiste = fields.Text('Scénario pessimiste')
    scenario_realiste = fields.Text('Scénario réaliste')
    
    # ========================================
    # STATUT ET SUIVI
    # ========================================
    state = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('en_cours', 'En cours d\'analyse'),
        ('termine', 'Terminé'),
        ('valide', 'Validé'),
        ('applique', 'Appliqué'),
        ('annule', 'Annulé')
    ], string='État', default='brouillon')
    
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes et observations')
    
    # ========================================
    # MÉTHODES IA AVANCÉES
    # ========================================
    
    @api.model_create_multi
    def create(self, vals_list):
        """Génération automatique du code unique"""
        for vals in vals_list:
            if not vals.get('code'):
                name = vals.get('name', 'PRED')
                code = name.upper().replace(' ', '_')[:15]
                counter = 1
                while self.search_count([('code', '=', code)]) > 0:
                    code = f"{name.upper().replace(' ', '_')[:12]}_{counter:03d}"
                    counter += 1
                vals['code'] = code
        return super().create(vals_list)
    
    def action_executer_prediction(self):
        """Exécute la prédiction IA selon le type"""
        self.ensure_one()
        
        try:
            _logger.info(f"Début de l'exécution de la prédiction IA: {self.name}")
            
            # Mise à jour du statut
            self.write({
                'state': 'en_cours',
                'date_execution': fields.Datetime.now()
            })
            
            # Exécution selon le type
            if self.type_prediction == 'rendement':
                self._predire_rendement()
            elif self.type_prediction == 'culture_optimale':
                self._recommander_culture_optimale()
            elif self.type_prediction == 'risque_climatique':
                self._evaluer_risques_climatiques()
            elif self.type_prediction == 'irrigation':
                self._optimiser_irrigation()
            elif self.type_prediction == 'engrais':
                self._optimiser_engrais()
            elif self.type_prediction == 'semis':
                self._optimiser_date_semis()
            elif self.type_prediction == 'recolte':
                self._optimiser_date_recolte()
            elif self.type_prediction == 'maladie':
                self._predire_maladies()
            elif self.type_prediction == 'stress_hydrique':
                self._evaluer_stress_hydrique()
            elif self.type_prediction == 'rotation_culturelle':
                self._planifier_rotation_culturelle()
            
            # Finalisation
            self.write({'state': 'termine'})
            
            _logger.info(f"Prédiction IA terminée avec succès: {self.name}")
            
        except Exception as e:
            _logger.error(f"Erreur lors de l'exécution de la prédiction IA: {str(e)}")
            self.write({'state': 'annule'})
            raise
    
    def _predire_rendement(self):
        """Prédiction du rendement basée sur l'IA avancée et l'historique des rendements"""
        try:
            # Récupération de l'historique des rendements pour cette exploitation/culture
            historique_rendements = self._obtenir_historique_rendements()
            
            # Modèle IA avancé basé sur plusieurs facteurs
            rendement_base = self._calculer_rendement_base()
            
            # Facteurs climatiques avancés
            facteurs_climatiques = self._analyser_facteurs_climatiques()
            
            # Facteurs pédologiques avancés
            facteurs_pedologiques = self._analyser_facteurs_pedologiques()
            
            # Facteurs culturaux et rotation
            facteurs_culturaux = self._analyser_facteurs_culturaux()
            
            # Facteurs de gestion et pratiques agricoles
            facteurs_gestion = self._analyser_facteurs_gestion()
            
            # Calcul du rendement prédit avec pondération IA
            rendement_predit = self._calculer_rendement_ia(
                rendement_base, facteurs_climatiques, facteurs_pedologiques, 
                facteurs_culturaux, facteurs_gestion, historique_rendements
            )
            
            # Calcul de la confiance et précision
            confiance, precision = self._calculer_metriques_ia(
                facteurs_climatiques, facteurs_pedologiques, facteurs_culturaux
            )
            
            # Mise à jour des résultats
            self.write({
                'rendement_predit': round(rendement_predit, 2),
                'rendement_optimal': round(rendement_predit * 1.15, 2),
                'gain_potentiel': round((rendement_predit - rendement_base) / rendement_base * 100, 1),
                'confiance': confiance,
                'precision': precision,
                'score_ia': (confiance + precision) / 2,
                'resultat_principal': f"Rendement prédit par IA avancée: {rendement_predit:.1f} t/ha",
                'resultat_detaille': self._generer_resultat_detaille_ia(
                    rendement_predit, facteurs_climatiques, facteurs_pedologiques, 
                    facteurs_culturaux, facteurs_gestion
                ),
                'recommandations': self._generer_recommandations_ia_avancees(
                    rendement_predit, facteurs_climatiques, facteurs_pedologiques
                ),
                'actions_prioritaires': self._generer_actions_prioritaires_ia(
                    rendement_predit, facteurs_climatiques, facteurs_pedologiques
                )
            })
            
        except Exception as e:
            _logger.error(f"Erreur lors de la prédiction IA avancée: {str(e)}")
            # Fallback vers la méthode simple
            self._predire_rendement_simple()
    
    def _obtenir_historique_rendements(self):
        """Récupère l'historique des rendements pour l'apprentissage IA"""
        domain = [
            ('exploitation_id', '=', self.exploitation_id.id),
            ('culture_id', '=', self.culture_id.id) if self.culture_id else [],
            ('rendement_reel', '>', 0),
            ('state', '=', 'termine')
        ]
        
        historique = self.search(domain, limit=10, order='date_creation desc')
        return historique
    
    def _calculer_rendement_base(self):
        """Calcule le rendement de base selon la culture et la zone"""
        rendement_base = 4.0  # Rendement de base par défaut
        
        if self.culture_id:
            # Rendements de base selon le type de culture
            if self.culture_id.type_culture == 'cereales':
                rendement_base = 6.0
            elif self.culture_id.type_culture == 'legumineuses':
                rendement_base = 3.5
            elif self.culture_id.type_culture == 'arboriculture':
                rendement_base = 8.0
            elif self.culture_id.type_culture == 'maraichage':
                rendement_base = 25.0
        
        # Ajustement selon la zone climatique
        if self.exploitation_id.zone_climatique == 'aride':
            rendement_base *= 0.7
        elif self.exploitation_id.zone_climatique == 'mediterraneen':
            rendement_base *= 1.1
        
        return rendement_base
    
    def _analyser_facteurs_climatiques(self):
        """Analyse avancée des facteurs climatiques"""
        facteurs = {
            'temperature': 1.0,
            'precipitation': 1.0,
            'humidite': 1.0,
            'vent': 1.0,
            'stress_climatique': 0.0
        }
        
        if self.temperature_moyenne:
            # Courbe de réponse optimale selon la culture
            if 18 <= self.temperature_moyenne <= 24:
                facteurs['temperature'] = 1.2
            elif 15 <= self.temperature_moyenne <= 27:
                facteurs['temperature'] = 1.1
            elif self.temperature_moyenne > 30 or self.temperature_moyenne < 10:
                facteurs['temperature'] = 0.6
                facteurs['stress_climatique'] += 0.3
        
        if self.precipitation_totale:
            # Analyse des précipitations avec seuils critiques
            if 400 <= self.precipitation_totale <= 700:
                facteurs['precipitation'] = 1.15
            elif 300 <= self.precipitation_totale <= 800:
                facteurs['precipitation'] = 1.05
            elif self.precipitation_totale < 200:
                facteurs['precipitation'] = 0.5
                facteurs['stress_climatique'] += 0.4
            elif self.precipitation_totale > 1000:
                facteurs['precipitation'] = 0.8
                facteurs['stress_climatique'] += 0.2
        
        return facteurs
    
    def _analyser_facteurs_pedologiques(self):
        """Analyse avancée des facteurs pédologiques"""
        facteurs = {
            'ph': 1.0,
            'azote': 1.0,
            'phosphore': 1.0,
            'potassium': 1.0,
            'structure': 1.0
        }
        
        if self.ph_sol:
            # Courbe de réponse optimale du pH
            if 6.2 <= self.ph_sol <= 7.2:
                facteurs['ph'] = 1.2
            elif 5.8 <= self.ph_sol <= 7.8:
                facteurs['ph'] = 1.1
            elif self.ph_sol < 5.5 or self.ph_sol > 8.5:
                facteurs['ph'] = 0.7
        
        if self.azote_sol:
            # Réponse à l'azote selon les besoins de la culture
            if 80 <= self.azote_sol <= 120:
                facteurs['azote'] = 1.15
            elif 60 <= self.azote_sol <= 150:
                facteurs['azote'] = 1.05
            elif self.azote_sol < 40:
                facteurs['azote'] = 0.6
            elif self.azote_sol > 200:
                facteurs['azote'] = 0.9
        
        return facteurs
    
    def _analyser_facteurs_culturaux(self):
        """Analyse des facteurs culturaux et de rotation"""
        facteurs = {
            'stade': 1.0,
            'rotation': 1.0,
            'diversite': 1.0
        }
        
        # Analyse du stade de développement
        if self.stade_culture:
            stades_optimaux = ['floraison', 'maturation']
            if self.stade_culture in stades_optimaux:
                facteurs['stade'] = 1.1
        
        # Analyse de la rotation culturelle
        if self.exploitation_id:
            rotations = self.env['smart_agri_rotation_culturelle'].search([
                ('exploitation_id', '=', self.exploitation_id.id),
                ('state', '=', 'en_cours')
            ])
            if rotations:
                # Amélioration : Gestion sécurisée du score de rotation
                scores_rotation = rotations.mapped('score_rotation')
                if scores_rotation:
                    score_moyen = sum(scores_rotation) / len(scores_rotation)
                    if score_moyen > 70:
                        facteurs['rotation'] = 1.15
                    elif score_moyen > 50:
                        facteurs['rotation'] = 1.05
                    else:
                        facteurs['rotation'] = 0.95  # Amélioration : Gestion des scores faibles
        
        return facteurs
    
    def _analyser_facteurs_gestion(self):
        """Analyse des facteurs de gestion et pratiques agricoles"""
        facteurs = {
            'irrigation': 1.0,
            'fertilisation': 1.0,
            'protection': 1.0
        }
        
        # Analyse de l'irrigation
        if self.eau_optimale and self.precipitation_totale:
            ratio_eau = self.precipitation_totale / self.eau_optimale
            if 0.8 <= ratio_eau <= 1.2:
                facteurs['irrigation'] = 1.1
            elif ratio_eau < 0.6:
                facteurs['irrigation'] = 0.7
            elif ratio_eau > 1.5:
                facteurs['irrigation'] = 0.9
        
        return facteurs
    
    def _calculer_rendement_ia(self, rendement_base, facteurs_climatiques, 
                               facteurs_pedologiques, facteurs_culturaux, facteurs_gestion, historique):
        """Calcul du rendement final avec pondération IA"""
        # Pondération des facteurs selon leur importance
        poids = {
            'climat': 0.35,
            'sol': 0.25,
            'culture': 0.20,
            'gestion': 0.20
        }
        
        # Calcul des scores pondérés
        score_climat = (
            facteurs_climatiques['temperature'] * 0.4 +
            facteurs_climatiques['precipitation'] * 0.4 +
            (1 - facteurs_climatiques['stress_climatique']) * 0.2
        )
        
        score_sol = (
            facteurs_pedologiques['ph'] * 0.3 +
            facteurs_pedologiques['azote'] * 0.4 +
            facteurs_pedologiques['phosphore'] * 0.2 +
            facteurs_pedologiques['potassium'] * 0.1
        )
        
        score_culture = (
            facteurs_culturaux['stade'] * 0.5 +
            facteurs_culturaux['rotation'] * 0.3 +
            facteurs_culturaux['diversite'] * 0.2
        )
        
        score_gestion = (
            facteurs_gestion['irrigation'] * 0.4 +
            facteurs_gestion['fertilisation'] * 0.4 +
            facteurs_gestion['protection'] * 0.2
        )
        
        # Facteur d'apprentissage basé sur l'historique
        facteur_apprentissage = 1.0
        if historique:
            rendements_historiques = historique.mapped('rendement_reel')
            if rendements_historiques:
                rendement_moyen_historique = sum(rendements_historiques) / len(rendements_historiques)
                facteur_apprentissage = rendement_moyen_historique / rendement_base
        
        # Calcul final du rendement
        rendement_final = rendement_base * (
            score_climat * poids['climat'] +
            score_sol * poids['sol'] +
            score_culture * poids['culture'] +
            score_gestion * poids['gestion']
        ) * facteur_apprentissage
        
        return max(rendement_final, 0.1)  # Rendement minimum
    
    def _calculer_metriques_ia(self, facteurs_climatiques, facteurs_pedologiques, facteurs_culturaux):
        """Calcule la confiance et précision de l'IA"""
        # Confiance basée sur la qualité des données
        confiance = 70.0
        
        if all([self.temperature_moyenne, self.precipitation_totale, self.ph_sol]):
            confiance += 15
        
        if self.culture_id:
            confiance += 10
        
        # Précision basée sur la stabilité des facteurs
        precision = 75.0
        
        if facteurs_climatiques['stress_climatique'] < 0.2:
            precision += 10
        
        if facteurs_pedologiques['ph'] > 0.9:
            precision += 10
        
        return min(confiance, 95), min(precision, 90)
    
    def _generer_resultat_detaille_ia(self, rendement_predit, facteurs_climatiques, 
                                      facteurs_pedologiques, facteurs_culturaux, facteurs_gestion):
        """Génère un résultat détaillé de l'analyse IA"""
        return f"""ANALYSE IA COMPLÈTE - RENDEMENT PRÉDIT: {rendement_predit:.1f} t/ha

🌡️ FACTEURS CLIMATIQUES:
- Température: {facteurs_climatiques.get('temperature', 'N/A')}
- Précipitations: {facteurs_climatiques.get('precipitation', 'N/A')}
- Stress climatique: {facteurs_climatiques.get('stress_climatique', 'N/A')}

🌱 FACTEURS PÉDOLOGIQUES:
- pH du sol: {facteurs_pedologiques.get('ph', 'N/A')}
- Azote: {facteurs_pedologiques.get('azote', 'N/A')}
- Phosphore: {facteurs_pedologiques.get('phosphore', 'N/A')}

🌾 FACTEURS CULTURAUX:
- Stade de développement: {facteurs_culturaux.get('stade', 'N/A')}
- Rotation: {facteurs_culturaux.get('rotation', 'N/A')}

⚡ FACTEURS DE GESTION:
- Irrigation: {facteurs_gestion.get('irrigation', 'N/A')}
- Fertilisation: {facteurs_gestion.get('fertilisation', 'N/A')}"""
    
    def _generer_recommandations_ia_avancees(self, rendement_predit, facteurs_climatiques, facteurs_pedologiques):
        """Génère des recommandations IA avancées"""
        recommandations = []
        
        if facteurs_climatiques['stress_climatique'] > 0.3:
            recommandations.append("🚨 Stress climatique élevé détecté. Actions d'urgence recommandées.")
        
        if facteurs_pedologiques['azote'] < 0.8:
            recommandations.append("🌱 Déficit en azote détecté. Apport d'engrais azoté recommandé.")
        
        if facteurs_pedologiques['ph'] < 0.8:
            recommandations.append("🧪 pH du sol suboptimal. Chaulage recommandé.")
        
        if facteurs_climatiques['precipitation'] < 0.7:
            recommandations.append("💧 Déficit hydrique. Irrigation d'appoint nécessaire.")
        
        return "\n".join(recommandations) if recommandations else "✅ Conditions optimales détectées."
    
    def _generer_actions_prioritaires_ia(self, rendement_predit, facteurs_climatiques, facteurs_pedologiques):
        """Génère des actions prioritaires basées sur l'IA"""
        actions = []
        
        if facteurs_climatiques['stress_climatique'] > 0.3:
            actions.append("1. 🚨 Mettre en place des mesures de protection contre le stress climatique")
        
        if facteurs_pedologiques['azote'] < 0.8:
            actions.append("2. 🌱 Planifier l'apport d'engrais azoté dans les 15 jours")
        
        if facteurs_pedologiques['ph'] < 0.8:
            actions.append("3. 🧪 Programmer le chaulage pour la prochaine saison")
        
        if facteurs_climatiques['precipitation'] < 0.7:
            actions.append("4. 💧 Activer le système d'irrigation d'appoint")
        
        actions.append("5. 📊 Surveiller quotidiennement les indicateurs de performance")
        actions.append("6. 🔄 Ajuster les pratiques culturales selon les recommandations IA")
        
        return "\n".join(actions)
    
    def _predire_rendement_simple(self):
        """Méthode de fallback pour la prédiction simple"""
        # Logique simplifiée en cas d'erreur de l'IA avancée
        if self.temperature_moyenne and self.precipitation_totale:
            base_rendement = 4.0
            facteur_temp = 1.0 if 15 <= self.temperature_moyenne <= 25 else 0.8
            facteur_precip = 1.0 if 300 <= self.precipitation_totale <= 600 else 0.7
            
            rendement = base_rendement * facteur_temp * facteur_precip
            
            self.write({
                'rendement_predit': round(rendement, 2),
                'rendement_optimal': round(rendement * 1.1, 2),
                'confiance': 60.0,
                'precision': 55.0,
                'score_ia': 57.5
            })
    
    def _recommander_culture_optimale(self):
        """Recommandation de culture optimale selon l'IA"""
        # Analyse des conditions pour recommander la meilleure culture
        recommandations = []
        
        if self.temperature_moyenne and self.precipitation_totale:
            if self.temperature_moyenne >= 20 and self.precipitation_totale >= 400:
                culture_recommandee = "Maïs"
                confiance = 90.0
            elif 15 <= self.temperature_moyenne <= 22 and 300 <= self.precipitation_totale <= 500:
                culture_recommandee = "Blé dur"
                confiance = 85.0
            elif self.temperature_moyenne >= 25 and self.precipitation_totale >= 600:
                culture_recommandee = "Riz"
                confiance = 88.0
            else:
                culture_recommandee = "Orge"
                confiance = 75.0
            
            self.write({
                'resultat_principal': f"Culture optimale recommandée: {culture_recommandee}",
                'confiance': confiance,
                'precision': confiance - 5.0,
                'score_ia': confiance,
                'recommandations': f"""
                Recommandation IA pour {culture_recommandee}:
                - Température optimale: {self.temperature_moyenne}°C
                - Précipitations optimales: {self.precipitation_totale}mm
                - Période de semis recommandée: Selon le calendrier cultural
                - Besoins en eau: Adaptés aux conditions locales
                """,
                'actions_prioritaires': f"""
                Actions pour {culture_recommandee}:
                1. Préparer le sol selon les exigences de {culture_recommandee}
                2. Planifier la date de semis optimale
                3. Organiser l'irrigation et la fertilisation
                4. Surveiller le développement et les maladies
                """
            })
    
    def _evaluer_risques_climatiques(self):
        """Évaluation des risques climatiques par l'IA"""
        risques = []
        niveau_risque = 'faible'
        
        if self.temperature_moyenne:
            if self.temperature_moyenne > 35:
                risques.append("Canicule - risque élevé de stress thermique")
                niveau_risque = 'eleve'
            elif self.temperature_moyenne < 5:
                risques.append("Gel - risque de dommages aux cultures")
                niveau_risque = 'modere'
        
        if self.precipitation_totale:
            if self.precipitation_totale < 200:
                risques.append("Sécheresse - déficit hydrique important")
                niveau_risque = 'eleve'
            elif self.precipitation_totale > 800:
                risques.append("Excès d'eau - risque d'asphyxie racinaire")
                niveau_risque = 'modere'
        
        if self.vitesse_vent and self.vitesse_vent > 50:
            risques.append("Vents forts - risque de verse et d'érosion")
            niveau_risque = 'modere'
        
        # Détermination du type de risque principal
        type_risque = 'secheresse'
        if 'canicule' in str(risques):
            type_risque = 'canicule'
        elif 'gel' in str(risques):
            type_risque = 'gel'
        elif 'excès d\'eau' in str(risques):
            type_risque = 'exces_eau'
        
        self.write({
            'niveau_risque': niveau_risque,
            'type_risque': type_risque,
            'resultat_principal': f"Évaluation des risques climatiques - Niveau: {niveau_risque.title()}",
            'confiance': 80.0,
            'precision': 75.0,
            'score_ia': 77.5,
            'resultat_detaille': f"""
            Analyse des risques climatiques:
            {chr(10).join(f"- {risque}" for risque in risques)}
            """,
            'recommandations': """
            Mesures de prévention recommandées:
            1. Surveiller les prévisions météo
            2. Adapter les pratiques culturales
            3. Renforcer l'irrigation si nécessaire
            4. Préparer les protections contre les aléas
            """,
            'actions_prioritaires': """
            Actions immédiates:
            1. Évaluer l'état des cultures
            2. Ajuster l'irrigation
            3. Préparer les protections
            4. Surveiller l'évolution météo
            """
        })
    
    def _optimiser_irrigation(self):
        """Optimisation de l'irrigation par l'IA"""
        if self.precipitation_totale and self.capacite_retention:
            # Calcul des besoins en eau
            besoins_base = 500  # mm/an
            deficit = max(0, besoins_base - self.precipitation_totale)
            
            # Optimisation selon le sol
            efficacite_irrigation = 0.8
            if self.type_sol == 'argileux':
                efficacite_irrigation = 0.9
            elif self.type_sol == 'sableux':
                efficacite_irrigation = 0.7
            
            eau_optimale = deficit / efficacite_irrigation
            
            self.write({
                'eau_optimale': round(eau_optimale, 1),
                'resultat_principal': f"Besoins en eau optimaux: {eau_optimale:.1f} m³/ha",
                'confiance': 85.0,
                'precision': 80.0,
                'score_ia': 82.5,
                'recommandations': f"""
                Optimisation de l'irrigation:
                - Déficit hydrique: {deficit:.1f} mm
                - Efficacité d'irrigation: {efficacite_irrigation * 100:.0f}%
                - Besoins totaux: {eau_optimale:.1f} m³/ha
                """,
                'actions_prioritaires': """
                Plan d'irrigation optimal:
                1. Répartir l'irrigation sur la saison
                2. Adapter aux stades de développement
                3. Surveiller l'humidité du sol
                4. Optimiser les horaires d'irrigation
                """
            })
    
    def _optimiser_engrais(self):
        """Optimisation des engrais par l'IA"""
        # Calcul des besoins en engrais selon le sol et la culture
        besoins_azote = 120  # kg/ha
        besoins_phosphore = 60  # kg/ha
        besoins_potassium = 80  # kg/ha
        
        # Ajustements selon le sol
        if self.azote_sol:
            besoins_azote = max(0, besoins_azote - self.azote_sol * 0.5)
        if self.phosphore_sol:
            besoins_phosphore = max(0, besoins_phosphore - self.phosphore_sol * 0.6)
        if self.potassium_sol:
            besoins_potassium = max(0, besoins_potassium - self.potassium_sol * 0.7)
        
        self.write({
            'engrais_azote': round(besoins_azote, 1),
            'engrais_phosphore': round(besoins_phosphore, 1),
            'engrais_potassium': round(besoins_potassium, 1),
            'resultat_principal': f"Optimisation des engrais: N={besoins_azote:.0f}, P={besoins_phosphore:.0f}, K={besoins_potassium:.0f} kg/ha",
            'confiance': 88.0,
            'precision': 82.0,
            'score_ia': 85.0,
            'recommandations': f"""
            Plan de fertilisation optimisé:
            - Azote: {besoins_azote:.0f} kg/ha
            - Phosphore: {besoins_phosphore:.0f} kg/ha
            - Potassium: {besoins_potassium:.0f} kg/ha
            """,
            'actions_prioritaires': """
            Application des engrais:
            1. Répartir l'azote sur la saison
            2. Appliquer le phosphore au semis
            3. Ajuster selon les analyses de sol
            4. Surveiller la réponse des cultures
            """
        })
    
    def _optimiser_date_semis(self):
        """Optimisation de la date de semis par l'IA"""
        # Calcul de la date optimale selon les conditions
        date_optimale = fields.Date.today()
        
        if self.temperature_moyenne:
            if self.temperature_moyenne < 10:
                date_optimale = fields.Date.today() + timedelta(days=30)
            elif self.temperature_moyenne > 25:
                date_optimale = fields.Date.today() - timedelta(days=15)
        
        self.write({
            'resultat_principal': f"Date optimale de semis: {date_optimale.strftime('%d/%m/%Y')}",
            'confiance': 82.0,
            'precision': 78.0,
            'score_ia': 80.0,
            'recommandations': f"""
            Optimisation de la date de semis:
            - Date recommandée: {date_optimale.strftime('%d/%m/%Y')}
            - Conditions optimales: Température 15-20°C
            - Précipitations: 20-40mm avant semis
            """,
            'actions_prioritaires': """
            Préparation au semis:
            1. Préparer le sol 2-3 semaines avant
            2. Surveiller les prévisions météo
            3. Ajuster selon l'humidité du sol
            4. Organiser le matériel et la main d'œuvre
            """
        })
    
    def _optimiser_date_recolte(self):
        """Optimisation de la date de récolte par l'IA"""
        # Calcul de la date optimale de récolte
        date_optimale = fields.Date.today() + timedelta(days=120)
        
        self.write({
            'resultat_principal': f"Date optimale de récolte: {date_optimale.strftime('%d/%m/%Y')}",
            'confiance': 85.0,
            'precision': 80.0,
            'score_ia': 82.5,
            'recommandations': f"""
            Optimisation de la date de récolte:
            - Date recommandée: {date_optimale.strftime('%d/%m/%Y')}
            - Critères: Maturité physiologique, conditions météo
            - Éviter: Pluies, humidité excessive
            """,
            'actions_prioritaires': """
            Préparation à la récolte:
            1. Surveiller la maturité des cultures
            2. Vérifier les prévisions météo
            3. Préparer le matériel de récolte
            4. Organiser le stockage et la logistique
            """
        })
    
    def _predire_maladies(self):
        """Prédiction des maladies par l'IA"""
        # Analyse des conditions favorables aux maladies
        maladies_risque = []
        
        if self.humidite_moyenne and self.humidite_moyenne > 80:
            maladies_risque.append("Mildiou - conditions humides favorables")
        
        if self.temperature_moyenne and 20 <= self.temperature_moyenne <= 30:
            maladies_risque.append("Rouille - température optimale")
        
        if self.precipitation_totale and self.precipitation_totale > 600:
            maladies_risque.append("Septoriose - excès d'humidité")
        
        niveau_risque = 'faible'
        if len(maladies_risque) >= 2:
            niveau_risque = 'eleve'
        elif len(maladies_risque) == 1:
            niveau_risque = 'modere'
        
        self.write({
            'niveau_risque': niveau_risque,
            'type_risque': 'maladie',
            'resultat_principal': f"Prédiction des maladies - Niveau: {niveau_risque.title()}",
            'confiance': 78.0,
            'precision': 72.0,
            'score_ia': 75.0,
            'resultat_detaille': f"""
            Analyse des risques de maladies:
            {chr(10).join(f"- {maladie}" for maladie in maladies_risque)}
            """,
            'recommandations': """
            Prévention des maladies:
            1. Surveiller les conditions météo
            2. Appliquer des traitements préventifs
            3. Améliorer l'aération des cultures
            4. Rotation des cultures
            """,
            'actions_prioritaires': """
            Actions préventives:
            1. Vérifier l'état sanitaire des cultures
            2. Planifier les traitements préventifs
            3. Optimiser la densité de plantation
            4. Surveiller l'apparition des premiers symptômes
            """
        })
    
    def _evaluer_stress_hydrique(self):
        """Évaluation du stress hydrique par l'IA"""
        # Calcul de l'indice de stress hydrique
        stress_index = 0
        
        if self.precipitation_totale:
            if self.precipitation_totale < 300:
                stress_index += 40
            elif self.precipitation_totale < 500:
                stress_index += 20
        
        if self.temperature_moyenne and self.temperature_moyenne > 30:
            stress_index += 30
        
        if self.humidite_moyenne and self.humidite_moyenne < 60:
            stress_index += 20
        
        # Classification du stress
        if stress_index >= 60:
            niveau_risque = 'critique'
        elif stress_index >= 40:
            niveau_risque = 'eleve'
        elif stress_index >= 20:
            niveau_risque = 'modere'
        else:
            niveau_risque = 'faible'
        
        self.write({
            'niveau_risque': niveau_risque,
            'type_risque': 'stress_hydrique',
            'resultat_principal': f"Stress hydrique - Niveau: {niveau_risque.title()} (Index: {stress_index})",
            'confiance': 85.0,
            'precision': 80.0,
            'score_ia': 82.5,
            'resultat_detaille': f"""
            Évaluation du stress hydrique:
            - Index de stress: {stress_index}/100
            - Précipitations: {self.precipitation_totale}mm
            - Température: {self.temperature_moyenne}°C
            - Humidité: {self.humidite_moyenne}%
            """,
            'recommandations': """
            Gestion du stress hydrique:
            1. Augmenter l'irrigation si possible
            2. Réduire la densité de plantation
            3. Appliquer du paillage
            4. Surveiller l'état des cultures
            """,
            'actions_prioritaires': """
            Actions immédiates:
            1. Évaluer l'urgence de l'irrigation
            2. Ajuster le calendrier cultural
            3. Préparer les mesures d'urgence
            4. Surveiller l'évolution des conditions
            """
        })
    
    def _planifier_rotation_culturelle(self):
        """Planification de la rotation culturelle par l'IA"""
        # Plan de rotation optimisé
        plan_rotation = """
        Plan de rotation culturelle optimisé:
        
        Année 1: Céréales (Blé/Orge)
        - Améliore la structure du sol
        - Réduit les maladies
        
        Année 2: Légumineuses (Pois/Fèves)
        - Fixe l'azote atmosphérique
        - Améliore la fertilité
        
        Année 3: Cultures sarclées (Maïs/Colza)
        - Désherbage naturel
        - Diversification des revenus
        
        Année 4: Jachère ou engrais verts
        - Régénération du sol
        - Réduction des parasites
        """
        
        self.write({
            'resultat_principal': "Plan de rotation culturelle optimisé sur 4 ans",
            'confiance': 88.0,
            'precision': 85.0,
            'score_ia': 86.5,
            'resultat_detaille': plan_rotation,
            'recommandations': """
            Avantages de cette rotation:
            1. Améliore la fertilité du sol
            2. Réduit les maladies et ravageurs
            3. Optimise l'utilisation des ressources
            4. Diversifie les revenus
            """,
            'actions_prioritaires': """
            Mise en œuvre de la rotation:
            1. Planifier les cultures sur 4 ans
            2. Adapter les rotations selon le marché
            3. Surveiller la santé du sol
            4. Ajuster selon les résultats
            """
        })
    
    def action_valider_prediction(self):
        """Valide la prédiction IA"""
        self.ensure_one()
        if self.state == 'termine':
            self.write({'state': 'valide'})
    
    def action_appliquer_prediction(self):
        """Marque la prédiction comme appliquée"""
        self.ensure_one()
        if self.state == 'valide':
            self.write({'state': 'applique'})
    
    def action_annuler_prediction(self):
        """Annule la prédiction"""
        self.ensure_one()
        self.write({'state': 'annule'})
    
    def action_dupliquer_prediction(self):
        """Duplique la prédiction pour une nouvelle analyse"""
        self.ensure_one()
        
        # Création d'une copie
        nouvelle_prediction = self.copy({
            'name': f"Copie - {self.name}",
            'state': 'brouillon',
            'date_creation': fields.Datetime.now(),
            'date_execution': False,
            'resultat_principal': '',
            'resultat_detaille': '',
            'recommandations': '',
            'actions_prioritaires': '',
            'confiance': 0.0,
            'precision': 0.0,
            'score_ia': 0.0
        })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_ia_predictions',
            'res_id': nouvelle_prediction.id,
            'view_mode': 'form',
            'target': 'current'
        }
