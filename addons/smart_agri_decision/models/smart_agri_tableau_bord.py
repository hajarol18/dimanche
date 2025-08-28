# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class SmartAgriTableauBord(models.Model):
    """Tableau de bord intelligent pour l'aide à la décision agricole"""

    _name = 'smart_agri_tableau_bord'
    _description = 'Tableau de Bord Intelligent SmartAgri'
    _auto = False  # Vue SQL personnalisée

    # ========================================
    # CHAMPS D'IDENTIFICATION
    # ========================================
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation')
    
    # ========================================
    # MÉTRIQUES DE PERFORMANCE GLOBALES
    # ========================================
    rendement_moyen = fields.Float('Rendement moyen (t/ha)', digits=(10, 2))
    rendement_optimal = fields.Float('Rendement optimal (t/ha)', digits=(10, 2))
    taux_realisation = fields.Float('Taux de réalisation (%)', digits=(5, 2))
    evolution_rendement = fields.Float('Évolution rendement (%)', digits=(5, 2))
    
    # ========================================
    # INDICATEURS CLIMATIQUES
    # ========================================
    temperature_moyenne = fields.Float('Température moyenne (°C)', digits=(5, 2))
    precipitation_totale = fields.Float('Précipitations totales (mm)', digits=(8, 2))
    risque_secheresse = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('critique', 'Critique')
    ], string='Risque de sécheresse')
    indice_climatique = fields.Float('Indice climatique (%)', digits=(5, 2))
    
    # ========================================
    # INDICATEURS DE QUALITÉ DU SOL
    # ========================================
    ph_sol_moyen = fields.Float('pH moyen du sol', digits=(4, 2))
    azote_sol_moyen = fields.Float('Azote moyen (kg/ha)', digits=(8, 2))
    phosphore_sol_moyen = fields.Float('Phosphore moyen (kg/ha)', digits=(8, 2))
    potassium_sol_moyen = fields.Float('Potassium moyen (kg/ha)', digits=(8, 2))
    indice_qualite_sol = fields.Float('Indice qualité sol (%)', digits=(5, 2))
    
    # ========================================
    # INDICATEURS DE ROTATION ET BIODIVERSITÉ
    # ========================================
    score_rotation_moyen = fields.Float('Score rotation moyen (%)', digits=(5, 2))
    diversite_cultures = fields.Integer('Diversité des cultures')
    cycle_rotation = fields.Integer('Cycle de rotation (années)')
    indice_biodiversite = fields.Float('Indice biodiversité (%)', digits=(5, 2))
    
    # ========================================
    # INDICATEURS ÉCONOMIQUES ET FINANCIERS
    # ========================================
    cout_intrants = fields.Float('Coût intrants (MAD/ha)', digits=(10, 2))
    revenu_attendu = fields.Float('Revenu attendu (MAD/ha)', digits=(10, 2))
    marge_brute = fields.Float('Marge brute (MAD/ha)', digits=(10, 2))
    rentabilite = fields.Float('Rentabilité (%)', digits=(5, 2))
    
    # ========================================
    # EFFICACITÉ OPÉRATIONNELLE
    # ========================================
    cout_par_hectare = fields.Float('Coût par hectare (MAD/ha)', digits=(10, 2))
    productivite_main_oeuvre = fields.Float('Productivité main d\'œuvre (MAD/h)', digits=(10, 2))
    efficacite_irrigation = fields.Float('Efficacité irrigation (%)', digits=(5, 2))
    optimisation_ressources = fields.Float('Optimisation ressources (%)', digits=(5, 2))
    
    # ========================================
    # INTELLIGENCE ARTIFICIELLE ET RECOMMANDATIONS
    # ========================================
    alertes_actives = fields.Integer('Alertes actives')
    recommandations_ia = fields.Text('Recommandations IA')
    actions_prioritaires = fields.Text('Actions prioritaires')
    score_ia_global = fields.Float('Score IA global (%)', digits=(5, 2))
    
    # ========================================
    # PRÉDICTIONS ET SCÉNARIOS
    # ========================================
    prediction_rendement = fields.Float('Prédiction rendement (t/ha)', digits=(10, 2))
    risque_climatique = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('critique', 'Critique')
    ], string='Risque climatique')
    opportunites_identifiees = fields.Text('Opportunités identifiées')
    scenarios_recommandes = fields.Text('Scénarios recommandés')
    
    # ========================================
    # SUIVI TEMPOREL ET TENDANCES
    # ========================================
    tendance_rendement = fields.Selection([
        ('croissante', 'Croissante'),
        ('stable', 'Stable'),
        ('decroissante', 'Décroissante')
    ], string='Tendance rendement')
    tendance_couts = fields.Selection([
        ('croissante', 'Croissante'),
        ('stable', 'Stable'),
        ('decroissante', 'Décroissante')
    ], string='Tendance coûts')
    tendance_climat = fields.Selection([
        ('favorable', 'Favorable'),
        ('neutre', 'Neutre'),
        ('defavorable', 'Défavorable')
    ], string='Tendance climat')
    periode_analyse = fields.Char('Période d\'analyse')
    
    # ========================================
    # COMPARAISONS ET BENCHMARKS
    # ========================================
    comparaison_annee_precedente = fields.Float('Comparaison année précédente (%)', digits=(5, 2))
    benchmark_secteur = fields.Float('Benchmark secteur (%)', digits=(5, 2))
    objectifs_annuels = fields.Float('Objectifs annuels (%)', digits=(5, 2))
    progression_objectifs = fields.Text('Progression objectifs')
    
    # ========================================
    # MÉTHODES
    # ========================================
    
    def init(self):
        """Initialise la vue SQL du tableau de bord avec des données simulées"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        
        # Vue SQL simplifiée avec des données simulées pour la démonstration
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT 
                    e.id as exploitation_id,
                    
                    -- Métriques de performance simulées
                    (RANDOM() * 10 + 5)::numeric(10,2) as rendement_moyen,
                    (RANDOM() * 12 + 6)::numeric(10,2) as rendement_optimal,
                    (RANDOM() * 30 + 70)::numeric(5,2) as taux_realisation,
                    (RANDOM() * 20 - 10)::numeric(5,2) as evolution_rendement,
                    
                    -- Indicateurs climatiques simulés
                    (RANDOM() * 20 + 10)::numeric(5,2) as temperature_moyenne,
                    (RANDOM() * 100 + 50)::numeric(8,2) as precipitation_totale,
                    CASE 
                        WHEN RANDOM() > 0.7 THEN 'critique'
                        WHEN RANDOM() > 0.5 THEN 'eleve'
                        WHEN RANDOM() > 0.3 THEN 'modere'
                        ELSE 'faible'
                    END as risque_secheresse,
                    (RANDOM() * 40 + 60)::numeric(5,2) as indice_climatique,
                    
                    -- Qualité du sol simulée
                    (RANDOM() * 3 + 6)::numeric(4,2) as ph_sol_moyen,
                    (RANDOM() * 50 + 100)::numeric(8,2) as azote_sol_moyen,
                    (RANDOM() * 30 + 50)::numeric(8,2) as phosphore_sol_moyen,
                    (RANDOM() * 40 + 80)::numeric(8,2) as potassium_sol_moyen,
                    (RANDOM() * 30 + 70)::numeric(5,2) as indice_qualite_sol,
                    
                    -- Rotation et biodiversité simulées
                    (RANDOM() * 40 + 60)::numeric(5,2) as score_rotation_moyen,
                    FLOOR(RANDOM() * 5 + 3)::integer as diversite_cultures,
                    FLOOR(RANDOM() * 3 + 2)::integer as cycle_rotation,
                    (RANDOM() * 40 + 60)::numeric(5,2) as indice_biodiversite,
                    
                    -- Indicateurs économiques simulés
                    (RANDOM() * 200 + 300)::numeric(10,2) as cout_intrants,
                    (RANDOM() * 500 + 800)::numeric(10,2) as revenu_attendu,
                    (RANDOM() * 300 + 400)::numeric(10,2) as marge_brute,
                    (RANDOM() * 20 + 60)::numeric(5,2) as rentabilite,
                    
                    -- Efficacité opérationnelle simulée
                    (RANDOM() * 150 + 250)::numeric(10,2) as cout_par_hectare,
                    (RANDOM() * 20 + 30)::numeric(10,2) as productivite_main_oeuvre,
                    (RANDOM() * 30 + 70)::numeric(5,2) as efficacite_irrigation,
                    (RANDOM() * 25 + 65)::numeric(5,2) as optimisation_ressources,
                    
                    -- IA et recommandations simulées
                    FLOOR(RANDOM() * 5)::integer as alertes_actives,
                    'Recommandations IA pour demonstration' as recommandations_ia,
                    'Actions prioritaires identifiees' as actions_prioritaires,
                    (RANDOM() * 30 + 70)::numeric(5,2) as score_ia_global,
                    
                    -- Prédictions simulées
                    (RANDOM() * 8 + 6)::numeric(10,2) as prediction_rendement,
                    CASE 
                        WHEN RANDOM() > 0.7 THEN 'critique'
                        WHEN RANDOM() > 0.5 THEN 'eleve'
                        WHEN RANDOM() > 0.3 THEN 'modere'
                        ELSE 'faible'
                    END as risque_climatique,
                    'Opportunites identifiees' as opportunites_identifiees,
                    'Scenarios recommandes' as scenarios_recommandes,
                    
                    -- Tendances simulées
                    CASE 
                        WHEN RANDOM() > 0.6 THEN 'croissante'
                        WHEN RANDOM() > 0.3 THEN 'stable'
                        ELSE 'decroissante'
                    END as tendance_rendement,
                    CASE 
                        WHEN RANDOM() > 0.6 THEN 'croissante'
                        WHEN RANDOM() > 0.3 THEN 'stable'
                        ELSE 'decroissante'
                    END as tendance_couts,
                    CASE 
                        WHEN RANDOM() > 0.6 THEN 'favorable'
                        WHEN RANDOM() > 0.3 THEN 'neutre'
                        ELSE 'defavorable'
                    END as tendance_climat,
                    'Periode d analyse' as periode_analyse,
                    
                    -- Comparaisons simulées
                    (RANDOM() * 40 - 20)::numeric(5,2) as comparaison_annee_precedente,
                    (RANDOM() * 30 + 70)::numeric(5,2) as benchmark_secteur,
                    (RANDOM() * 40 + 60)::numeric(5,2) as objectifs_annuels,
                    'Progression des objectifs' as progression_objectifs
                    
                FROM smart_agri_exploitation e
                WHERE e.active = true
            )
        """ % self._table)
    
    # ========================================
    # MÉTHODES MÉTIER
    # ========================================
    
    def action_actualiser_donnees(self):
        """Actualise les données du tableau de bord"""
        self.init()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Données actualisées',
                'message': 'Le tableau de bord a été actualisé avec succès.',
                'type': 'success'
            }
        }
    
    def action_generer_rapport(self):
        """Génère un rapport PDF du tableau de bord"""
        return {
            'type': 'ir.actions.report',
            'report_name': 'smart_agri_decision.report_tableau_bord',
            'report_type': 'qweb-pdf',
            'data': {'tableau_bord_id': self.id}
        }
    
    def action_analyser_tendances(self):
        """Ouvre l'analyse des tendances"""
        return {
            'name': 'Analyse des Tendances',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_tableau_bord',
            'view_mode': 'graph,pivot',
            'domain': [('exploitation_id', '=', self.exploitation_id.id)],
            'context': {'default_exploitation_id': self.exploitation_id.id}
        }


class SmartAgriIndicateurPerformance(models.Model):
    """Indicateurs de performance pour le tableau de bord"""

    _name = 'smart_agri_indicateur_performance'
    _description = 'Indicateurs de Performance SmartAgri'
    _order = 'sequence, name'

    sequence = fields.Integer('Séquence', default=10)
    name = fields.Char('Nom de l\'indicateur', required=True)
    code = fields.Char('Code', required=True)
    
    # ========================================
    # DÉFINITION DE L'INDICATEUR
    # ========================================
    type_indicateur = fields.Selection([
        ('metrique', 'Métrique simple'),
        ('ratio', 'Ratio/Pourcentage'),
        ('evolution', 'Évolution temporelle'),
        ('comparaison', 'Comparaison'),
        ('alerte', 'Alerte/Seuil')
    ], string='Type d\'indicateur', required=True)
    
    formule_calcul = fields.Text('Formule de calcul')
    unite = fields.Char('Unité de mesure')
    seuil_alerte = fields.Float('Seuil d\'alerte')
    seuil_critique = fields.Float('Seuil critique')
    
    # ========================================
    # CATÉGORISATION
    # ========================================
    categorie = fields.Selection([
        ('productivite', 'Productivité'),
        ('qualite', 'Qualité'),
        ('durabilite', 'Durabilité'),
        ('economique', 'Économique'),
        ('environnemental', 'Environnemental'),
        ('social', 'Social')
    ], string='Catégorie', required=True)
    
    sous_categorie = fields.Char('Sous-catégorie')
    
    # ========================================
    # CONFIGURATION D'AFFICHAGE
    # ========================================
    couleur_positive = fields.Char('Couleur positive', default='#28a745')
    couleur_negative = fields.Char('Couleur négative', default='#dc3545')
    couleur_neutre = fields.Char('Couleur neutre', default='#6c757d')
    
    # ========================================
    # STATUT ET SUIVI
    # ========================================
    actif = fields.Boolean('Actif', default=True)
    description = fields.Text('Description détaillée')
    notes = fields.Text('Notes et observations')
    
    # ========================================
    # MÉTHODES
    # ========================================
    
    def calculer_valeur(self, exploitation_id=None, parcelle_id=None, date_debut=None, date_fin=None):
        """Calcule la valeur de l'indicateur selon les paramètres"""
        self.ensure_one()
        
        # Logique de calcul selon le type d'indicateur
        if self.type_indicateur == 'metrique':
            return self._calculer_metrique(exploitation_id, parcelle_id, date_debut, date_fin)
        elif self.type_indicateur == 'ratio':
            return self._calculer_ratio(exploitation_id, parcelle_id, date_debut, date_fin)
        elif self.type_indicateur == 'evolution':
            return self._calculer_evolution(exploitation_id, parcelle_id, date_debut, date_fin)
        else:
            return 0.0
    
    def _calculer_metrique(self, exploitation_id, parcelle_id, date_debut, date_fin):
        """Calcule une métrique simple"""
        domain = []
        if exploitation_id:
            domain.append(('exploitation_id', '=', exploitation_id))
        if parcelle_id:
            domain.append(('parcelle_id', '=', parcelle_id))
        if date_debut:
            domain.append(('date_creation', '>=', date_debut))
        if date_fin:
            domain.append(('date_creation', '<=', date_fin))
        
        # Exemple pour le rendement moyen
        if self.code == 'RENDEMENT_MOYEN':
            predictions = self.env['smart_agri_ia_predictions'].search(domain)
            if predictions:
                return sum(predictions.mapped('rendement_predit')) / len(predictions)
        
        return 0.0
    
    def _calculer_ratio(self, exploitation_id, parcelle_id, date_debut, date_fin):
        """Calcule un ratio"""
        # Logique de calcul de ratio
        return 0.0
    
    def _calculer_evolution(self, exploitation_id, parcelle_id, date_debut, date_fin):
        """Calcule l'évolution temporelle"""
        # Logique de calcul d'évolution
        return 0.0
    
    def evaluer_performance(self, valeur):
        """Évalue la performance selon les seuils"""
        if valeur >= self.seuil_alerte:
            return 'excellent'
        elif valeur >= self.seuil_critique:
            return 'bon'
        else:
            return 'critique'


class SmartAgriAlerte(models.Model):
    """Système d'alertes intelligentes"""

    _name = 'smart_agri_alerte'
    _description = 'Alertes Intelligentes SmartAgri'
    _order = 'priorite desc, date_creation desc'

    name = fields.Char('Nom de l\'alerte', required=True)
    code = fields.Char('Code unique', required=True, copy=False)
    
    # ========================================
    # TYPE ET PRIORITÉ
    # ========================================
    type_alerte = fields.Selection([
        ('climatique', 'Climatique'),
        ('agronomique', 'Agronomique'),
        ('economique', 'Économique'),
        ('technique', 'Technique'),
        ('securite', 'Sécurité')
    ], string='Type d\'alerte', required=True)
    
    priorite = fields.Selection([
        ('critique', 'Critique'),
        ('elevee', 'Élevée'),
        ('normale', 'Normale'),
        ('faible', 'Faible')
    ], string='Priorité', required=True, default='normale')
    
    # ========================================
    # CONTEXTE ET DÉTAILS
    # ========================================
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation')
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle')
    description = fields.Text('Description de l\'alerte')
    cause_racine = fields.Text('Cause racine')
    
    # ========================================
    # RECOMMANDATIONS ET ACTIONS
    # ========================================
    recommandations = fields.Text('Recommandations')
    actions_immediates = fields.Text('Actions immédiates')
    actions_preventives = fields.Text('Actions préventives')
    
    # ========================================
    # SUIVI ET STATUT
    # ========================================
    date_creation = fields.Datetime('Date de création', default=fields.Datetime.now)
    date_resolution = fields.Datetime('Date de résolution')
    state = fields.Selection([
        ('active', 'Active'),
        ('en_cours', 'En cours de résolution'),
        ('resolue', 'Résolue'),
        ('ignoree', 'Ignorée')
    ], string='État', default='active')
    
    # ========================================
    # MÉTHODES
    # ========================================
    
    def action_resoudre_alerte(self):
        """Marque l'alerte comme résolue"""
        self.ensure_one()
        self.write({
            'state': 'resolue',
            'date_resolution': fields.Datetime.now()
        })
        return True
    
    def action_ignorer_alerte(self):
        """Ignore l'alerte"""
        self.ensure_one()
        self.write({'state': 'ignoree'})
        return True
    
    def action_traiter_alerte(self):
        """Marque l'alerte comme en cours de traitement"""
        self.ensure_one()
        self.write({'state': 'en_cours'})
        return True
