# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class SmartAgriTendanceClimatique(models.Model):
    """Tendances climatiques historiques et projetées"""

    _name = 'smart_agri_tendance_climatique'
    _description = 'Tendances Climatiques'
    _order = 'date_debut desc'

    # RELATION PRINCIPALE - LOGIQUE MÉTIER
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True, ondelete='cascade')

    # Champs de base
    name = fields.Char('Nom de la tendance', required=True)
    description = fields.Text('Description de la tendance')
    
    # Type de tendance
    type_tendance = fields.Selection([
        ('historique', 'Historique'),
        ('projetee', 'Projetée'),
        ('comparaison', 'Comparaison historique/projetée')
    ], string='Type de tendance', required=True)
    
    # Période d'analyse
    date_debut = fields.Date('Date de début', required=True)
    date_fin = fields.Date('Date de fin', required=True)
    duree_periode = fields.Integer('Durée de la période (jours)', compute='_compute_duree', store=True)
    
    # Zone géographique
    zone_geographique = fields.Char('Zone géographique')
    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')
    
    # Paramètres climatiques analysés
    parametres_analyses = fields.Selection([
        ('temperature', 'Température'),
        ('precipitation', 'Précipitations'),
        ('humidite', 'Humidité'),
        ('ensoleillement', 'Ensoleillement'),
        ('vitesse_vent', 'Vitesse du vent'),
        ('tous', 'Tous les paramètres')
    ], string='Paramètres analysés', required=True)
    
    # Tendances observées
    tendance_temperature = fields.Selection([
        ('hausse', 'Hausse'),
        ('baisse', 'Baisse'),
        ('stable', 'Stable'),
        ('variable', 'Variable')
    ], string='Tendance température')
    
    tendance_precipitation = fields.Selection([
        ('hausse', 'Hausse'),
        ('baisse', 'Baisse'),
        ('stable', 'Stable'),
        ('variable', 'Variable')
    ], string='Tendance précipitations')
    
    tendance_humidite = fields.Selection([
        ('hausse', 'Hausse'),
        ('baisse', 'Baisse'),
        ('stable', 'Stable'),
        ('variable', 'Variable')
    ], string='Tendance humidité')
    
    # Valeurs numériques
    temperature_moyenne = fields.Float('Température moyenne (°C)')
    temperature_min = fields.Float('Température minimum (°C)')
    temperature_max = fields.Float('Température maximum (°C)')
    
    precipitation_totale = fields.Float('Précipitations totales (mm)')
    precipitation_moyenne = fields.Float('Précipitations moyennes (mm/jour)')
    
    humidite_moyenne = fields.Float('Humidité moyenne (%)')
    ensoleillement_moyen = fields.Float('Ensoleillement moyen (heures/jour)')
    vitesse_vent_moyenne = fields.Float('Vitesse du vent moyenne (km/h)')
    
    # Indices climatiques
    indice_secheresse = fields.Float('Indice de sécheresse')
    indice_pluviosite = fields.Float('Indice de pluviosité')
    indice_thermique = fields.Float('Indice thermique')
    
    # Scénarios RCP (selon le cahier des charges)
    rcp_scenario_id = fields.Many2one('smart_agri_rcp_scenario', string='Scénario RCP')
    
    # Impact agricole
    impact_agricole = fields.Selection([
        ('positif', 'Positif'),
        ('negatif', 'Négatif'),
        ('neutre', 'Neutre'),
        ('mixte', 'Mixte')
    ], string='Impact agricole global')
    
    cultures_favorisees = fields.Text('Cultures favorisées par cette tendance')
    cultures_defavorisees = fields.Text('Cultures défavorisées par cette tendance')
    
    # Recommandations d'adaptation
    recommandations_adaptation = fields.Text('Recommandations d\'adaptation')
    strategies_mitigation = fields.Text('Stratégies de mitigation')
    
    # Source des données
    source_donnees = fields.Selection([
        ('meteo_france', 'Météo France'),
        ('api_meteo', 'API Météo'),
        ('capteurs_locaux', 'Capteurs locaux'),
        ('satellite', 'Données satellite'),
        ('modele_climatique', 'Modèle climatique'),
        ('autre', 'Autre')
    ], string='Source des données', required=True)
    
    # Qualité des données
    qualite_donnees = fields.Selection([
        ('excellente', 'Excellente'),
        ('bonne', 'Bonne'),
        ('moyenne', 'Moyenne'),
        ('faible', 'Faible')
    ], string='Qualité des données', default='bonne')
    
    # Notes et documentation
    notes = fields.Text('Notes et observations')
    documentation = fields.Binary('Documentation technique')
    nom_fichier_doc = fields.Char('Nom du fichier')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    
    # Calcul de la durée
    @api.depends('date_debut', 'date_fin')
    def _compute_duree(self):
        for record in self:
            if record.date_debut and record.date_fin:
                delta = record.date_fin - record.date_debut
                record.duree_periode = delta.days
            else:
                record.duree_periode = 0
    
    # Calcul automatique du nom
    @api.depends('type_tendance', 'parametres_analyses', 'date_debut', 'date_fin')
    def _compute_name(self):
        for record in self:
            if record.type_tendance and record.parametres_analyses and record.date_debut and record.date_fin:
                record.name = f"Tendance {record.type_tendance.title()} - {record.parametres_analyses.title()} - {record.date_debut.strftime('%m/%Y')} à {record.date_fin.strftime('%m/%Y')}"
            else:
                record.name = "Nouvelle tendance climatique"
    
    # Méthode pour calculer les indices climatiques
    def calculer_indices(self):
        for record in self:
            # Calcul de l'indice de sécheresse (simplifié)
            if record.temperature_moyenne and record.precipitation_totale:
                record.indice_secheresse = record.temperature_moyenne / (record.precipitation_totale + 1)
            
            # Calcul de l'indice de pluviosité
            if record.precipitation_moyenne:
                record.indice_pluviosite = record.precipitation_moyenne * record.duree_periode
            
            # Calcul de l'indice thermique
            if record.temperature_moyenne:
                record.indice_thermique = record.temperature_moyenne * record.duree_periode
    
    # Méthode pour analyser l'impact agricole
    def analyser_impact_agricole(self):
        for record in self:
            impact_score = 0
            
            # Analyse basée sur les tendances
            if record.tendance_temperature == 'hausse':
                impact_score += 1
            elif record.tendance_temperature == 'baisse':
                impact_score -= 1
            
            if record.tendance_precipitation == 'hausse':
                impact_score += 1
            elif record.tendance_precipitation == 'baisse':
                impact_score -= 1
            
            # Détermination de l'impact global
            if impact_score > 0:
                record.impact_agricole = 'positif'
            elif impact_score < 0:
                record.impact_agricole = 'negatif'
            else:
                record.impact_agricole = 'neutre'
