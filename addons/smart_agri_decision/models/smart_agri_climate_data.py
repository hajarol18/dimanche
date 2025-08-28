# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta
import random
import math

_logger = logging.getLogger(__name__)


class SmartAgriClimateData(models.Model):
    """Données climatiques massives pour l'entraînement IA"""
    
    _name = 'smart_agri_climate_data'
    _description = 'Données Climatiques Massives'
    _order = 'date desc, parcelle_id'
    _rec_name = 'display_name'
    
    # RELATIONS
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle', required=True, ondelete='cascade')
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', related='parcelle_id.exploitation_id', store=True)
    
    # IDENTIFICATION TEMPORELLE
    date = fields.Date('Date', required=True, default=fields.Date.today)
    annee = fields.Integer('Année', compute='_compute_annee', store=True)
    mois = fields.Integer('Mois', compute='_compute_mois', store=True)
    jour = fields.Integer('Jour', compute='_compute_jour', store=True)
    saison = fields.Selection([
        ('hiver', 'Hiver'),
        ('printemps', 'Printemps'),
        ('ete', 'Été'),
        ('automne', 'Automne')
    ], string='Saison', compute='_compute_saison', store=True)
    
    # DONNÉES CLIMATIQUES BRUTES
    temperature_min = fields.Float('Température min (°C)', digits=(5, 2))
    temperature_max = fields.Float('Température max (°C)', digits=(5, 2))
    temperature_moy = fields.Float('Température moyenne (°C)', digits=(5, 2))
    humidite = fields.Float('Humidité relative (%)', digits=(5, 2))
    pression_atmospherique = fields.Float('Pression atmosphérique (hPa)', digits=(7, 2))
    vitesse_vent = fields.Float('Vitesse du vent (km/h)', digits=(5, 2))
    direction_vent = fields.Float('Direction du vent (°)', digits=(5, 1))
    rayonnement_solaire = fields.Float('Rayonnement solaire (W/m²)', digits=(6, 2))
    duree_ensoleillement = fields.Float('Durée d\'ensoleillement (h)', digits=(4, 2))
    
    # PRÉCIPITATIONS ET EAU
    precipitation = fields.Float('Précipitations (mm)', digits=(6, 2))
    precipitation_cumul_7j = fields.Float('Précipitations cumulées 7j (mm)', digits=(6, 2))
    precipitation_cumul_30j = fields.Float('Précipitations cumulées 30j (mm)', digits=(6, 2))
    evapotranspiration = fields.Float('Évapotranspiration (mm)', digits=(6, 2))
    deficit_hydrique = fields.Float('Déficit hydrique (mm)', digits=(6, 2))
    
    # INDICES CLIMATIQUES
    indice_aridite = fields.Float('Indice d\'aridité', digits=(4, 3))
    indice_thermique = fields.Float('Indice thermique', digits=(4, 2))
    indice_humidite = fields.Float('Indice d\'humidité', digits=(4, 3))
    stress_hydrique = fields.Selection([
        ('aucun', 'Aucun'),
        ('leger', 'Léger'),
        ('modere', 'Modéré'),
        ('severe', 'Sévère'),
        ('extreme', 'Extrême')
    ], string='Stress hydrique', compute='_compute_stress_hydrique', store=True)
    
    # SCÉNARIOS RCP (RÉCHAUFFEMENT CLIMATIQUE)
    scenario_rcp = fields.Selection([
        ('rcp26', 'RCP 2.6 (Optimiste)'),
        ('rcp45', 'RCP 4.5 (Modéré)'),
        ('rcp60', 'RCP 6.0 (Pessimiste)'),
        ('rcp85', 'RCP 8.5 (Très pessimiste)'),
        ('historique', 'Données historiques')
    ], string='Scénario RCP', default='historique', required=True)
    
    # PROJECTIONS CLIMATIQUES (2050, 2100)
    annee_projection = fields.Integer('Année de projection')
    temperature_projete = fields.Float('Température projetée (°C)', digits=(5, 2))
    precipitation_projetee = fields.Float('Précipitations projetées (mm)', digits=(6, 2))
    
    # ALERTES CLIMATIQUES
    alerte_gel = fields.Boolean('Alerte gel')
    alerte_secheresse = fields.Boolean('Alerte sécheresse')
    alerte_canicule = fields.Boolean('Alerte canicule')
    alerte_inondation = fields.Boolean('Alerte inondation')
    alerte_orage = fields.Boolean('Alerte orage')
    
    # MÉTADONNÉES
    source_donnees = fields.Selection([
        ('api_meteo', 'API Météo officielle'),
        ('station_locale', 'Station météo locale'),
        ('satellite', 'Données satellite'),
        ('modele_climatique', 'Modèle climatique'),
        ('interpolation', 'Interpolation spatiale'),
        ('simulation', 'Simulation IA')
    ], string='Source des données', default='api_meteo')
    
    qualite_donnees = fields.Selection([
        ('excellente', 'Excellente'),
        ('bonne', 'Bonne'),
        ('moyenne', 'Moyenne'),
        ('faible', 'Faible'),
        ('inconnue', 'Inconnue')
    ], string='Qualité des données', default='bonne')
    
    precision_spatiale = fields.Float('Précision spatiale (km)', digits=(4, 2))
    precision_temporelle = fields.Float('Précision temporelle (h)', digits=(4, 2))
    
    # STATUT
    active = fields.Boolean('Actif', default=True)
    valide = fields.Boolean('Données validées', default=False)
    notes = fields.Text('Notes et observations')
    
    # CHAMPS CALCULÉS
    display_name = fields.Char('Nom affiché', compute='_compute_display_name', store=True)
    
    @api.depends('date', 'parcelle_id.name', 'scenario_rcp')
    def _compute_display_name(self):
        for record in self:
            if record.date and record.parcelle_id:
                record.display_name = f"{record.parcelle_id.name} - {record.date} - {record.scenario_rcp}"
            else:
                record.display_name = "Nouvelle donnée climatique"
    
    @api.depends('date')
    def _compute_annee(self):
        for record in self:
            if record.date:
                record.annee = record.date.year
            else:
                record.annee = 0
    
    @api.depends('date')
    def _compute_mois(self):
        for record in self:
            if record.date:
                record.mois = record.date.month
            else:
                record.mois = 0
    
    @api.depends('date')
    def _compute_jour(self):
        for record in self:
            if record.date:
                record.jour = record.date.day
            else:
                record.jour = 0
    
    @api.depends('mois')
    def _compute_saison(self):
        for record in self:
            if record.mois in [12, 1, 2]:
                record.saison = 'hiver'
            elif record.mois in [3, 4, 5]:
                record.saison = 'printemps'
            elif record.mois in [6, 7, 8]:
                record.saison = 'ete'
            elif record.mois in [9, 10, 11]:
                record.saison = 'automne'
            else:
                record.saison = 'hiver'
    
    @api.depends('deficit_hydrique', 'indice_aridite')
    def _compute_stress_hydrique(self):
        for record in self:
            if record.deficit_hydrique and record.indice_aridite:
                if record.deficit_hydrique > 50 or record.indice_aridite > 0.8:
                    record.stress_hydrique = 'extreme'
                elif record.deficit_hydrique > 30 or record.indice_aridite > 0.6:
                    record.stress_hydrique = 'severe'
                elif record.deficit_hydrique > 15 or record.indice_aridite > 0.4:
                    record.stress_hydrique = 'modere'
                elif record.deficit_hydrique > 5 or record.indice_aridite > 0.2:
                    record.stress_hydrique = 'leger'
                else:
                    record.stress_hydrique = 'aucun'
            else:
                record.stress_hydrique = 'inconnue'
    
    # CONTRAINTES
    @api.constrains('date')
    def _check_date_future(self):
        for record in self:
            if record.date and record.date > fields.Date.today() and record.scenario_rcp == 'historique':
                raise ValidationError('Les données historiques ne peuvent pas être dans le futur.')
    
    @api.constrains('temperature_min', 'temperature_max')
    def _check_temperature_range(self):
        for record in self:
            if record.temperature_min and record.temperature_max:
                if record.temperature_min > record.temperature_max:
                    raise ValidationError('La température minimale ne peut pas être supérieure à la maximale.')
    
    @api.constrains('humidite')
    def _check_humidite_range(self):
        for record in self:
            if record.humidite and (record.humidite < 0 or record.humidite > 100):
                raise ValidationError('L\'humidité doit être comprise entre 0 et 100%.')
    
    # MÉTHODES MÉTIER
    def action_generer_donnees_historiques(self):
        """Génère des données climatiques historiques massives pour l'entraînement IA"""
        self.ensure_one()
        
        # Génération de 5 ans de données historiques
        date_debut = datetime(2019, 1, 1)
        date_fin = datetime(2024, 12, 31)
        
        donnees_generees = []
        date_courante = date_debut
        
        while date_courante <= date_fin:
            # Génération de données réalistes avec variations saisonnières
            donnee = self._generer_donnee_jour(date_courante.date())
            donnees_generees.append(donnee)
            date_courante += timedelta(days=1)
        
        # Création des enregistrements
        for donnee in donnees_generees:
            self.create(donnee)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Génération terminée',
                'message': f'{len(donnees_generees)} jours de données climatiques générés avec succès.',
                'type': 'success',
            }
        }
    
    def _generer_donnee_jour(self, date):
        """Génère des données climatiques réalistes pour une journée donnée"""
        mois = date.month
        jour_annee = date.timetuple().tm_yday
        
        # Variations saisonnières
        temp_base = 15 + 10 * math.sin(2 * math.pi * (jour_annee - 80) / 365)
        humidite_base = 70 - 20 * math.sin(2 * math.pi * (jour_annee - 80) / 365)
        
        # Variations journalières
        temp_min = temp_base - 5 + random.uniform(-2, 2)
        temp_max = temp_base + 5 + random.uniform(-2, 2)
        temp_moy = (temp_min + temp_max) / 2
        
        # Précipitations (plus fréquentes en hiver/printemps)
        proba_precip = 0.3 if mois in [1, 2, 3, 4, 11, 12] else 0.1
        precipitation = random.uniform(0, 20) if random.random() < proba_precip else 0
        
        return {
            'parcelle_id': self.parcelle_id.id,
            'date': date,
            'scenario_rcp': 'historique',
            'temperature_min': round(temp_min, 2),
            'temperature_max': round(temp_max, 2),
            'temperature_moy': round(temp_moy, 2),
            'humidite': round(humidite_base + random.uniform(-10, 10), 2),
            'precipitation': round(precipitation, 2),
            'pression_atmospherique': round(1013 + random.uniform(-20, 20), 2),
            'vitesse_vent': round(random.uniform(0, 30), 2),
            'rayonnement_solaire': round(max(0, 800 + random.uniform(-200, 200)), 2),
            'source_donnees': 'simulation',
            'qualite_donnees': 'bonne'
        }
    
    def action_generer_scenarios_rcp(self):
        """Génère des projections climatiques selon les scénarios RCP"""
        self.ensure_one()
        
        scenarios = ['rcp26', 'rcp45', 'rcp60', 'rcp85']
        annees_projection = [2030, 2050, 2070, 2100]
        
        for scenario in scenarios:
            for annee in annees_projection:
                # Calcul des projections selon le scénario
                temp_projete = self._calculer_projection_temperature(scenario, annee)
                precip_projetee = self._calculer_projection_precipitations(scenario, annee)
                
                self.create({
                    'parcelle_id': self.parcelle_id.id,
                    'date': fields.Date.today(),
                    'scenario_rcp': scenario,
                    'annee_projection': annee,
                    'temperature_projete': temp_projete,
                    'precipitation_projetee': precip_projetee,
                    'source_donnees': 'modele_climatique',
                    'qualite_donnees': 'moyenne'
                })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Scénarios RCP générés',
                'message': f'Projections climatiques générées pour {len(scenarios)} scénarios et {len(annees_projection)} années.',
                'type': 'success',
            }
        }
    
    def _calculer_projection_temperature(self, scenario, annee):
        """Calcule la projection de température selon le scénario RCP"""
        base_temp = 15  # Température de base actuelle
        
        # Facteurs de réchauffement selon RCP
        facteurs_rcp = {
            'rcp26': 0.3,  # +0.3°C par décennie
            'rcp45': 0.5,  # +0.5°C par décennie
            'rcp60': 0.7,  # +0.7°C par décennie
            'rcp85': 1.0   # +1.0°C par décennie
        }
        
        decennies = (annee - 2020) / 10
        augmentation = facteurs_rcp.get(scenario, 0.5) * decennies
        
        return round(base_temp + augmentation + random.uniform(-0.5, 0.5), 2)
    
    def _calculer_projection_precipitations(self, scenario, annee):
        """Calcule la projection de précipitations selon le scénario RCP"""
        base_precip = 800  # Précipitations de base annuelles (mm)
        
        # Variations selon RCP (plus d'incertitude)
        variations_rcp = {
            'rcp26': (-5, 10),    # -5% à +10%
            'rcp45': (-10, 15),   # -10% à +15%
            'rcp60': (-15, 20),   # -15% à +20%
            'rcp85': (-20, 25)    # -20% à +25%
        }
        
        min_var, max_var = variations_rcp.get(scenario, (-10, 15))
        variation = random.uniform(min_var, max_var) / 100
        
        return round(base_precip * (1 + variation), 2)
    
    # MÉTHODES D'ANALYSE POUR L'IA
    @api.model
    def get_donnees_entrainement_ia(self, parcelle_ids=None, date_debut=None, date_fin=None):
        """Récupère les données d'entraînement pour les modèles IA"""
        domain = [('active', '=', True), ('valide', '=', True)]
        
        if parcelle_ids:
            domain.append(('parcelle_id', 'in', parcelle_ids))
        if date_debut:
            domain.append(('date', '>=', date_debut))
        if date_fin:
            domain.append(('date', '<=', date_fin))
        
        donnees = self.search(domain, order='date asc')
        
        # Formatage pour l'entraînement IA
        features = []
        for donnee in donnees:
            feature_vector = {
                'date': donnee.date.isoformat(),
                'parcelle_id': donnee.parcelle_id.id,
                'temperature_min': donnee.temperature_min or 0,
                'temperature_max': donnee.temperature_max or 0,
                'temperature_moy': donnee.temperature_moy or 0,
                'humidite': donnee.humidite or 0,
                'precipitation': donnee.precipitation or 0,
                'evapotranspiration': donnee.evapotranspiration or 0,
                'deficit_hydrique': donnee.deficit_hydrique or 0,
                'indice_aridite': donnee.indice_aridite or 0,
                'mois': donnee.mois,
                'saison': donnee.saison,
                'scenario_rcp': donnee.scenario_rcp
            }
            features.append(feature_vector)
        
        return features
    
    @api.model
    def get_statistiques_climatiques(self, parcelle_id, annee=None):
        """Calcule les statistiques climatiques pour une parcelle"""
        domain = [('parcelle_id', '=', parcelle_id), ('active', '=', True)]
        if annee:
            domain.append(('annee', '=', annee))
        
        donnees = self.search(domain)
        
        if not donnees:
            return {}
        
        stats = {
            'nb_jours': len(donnees),
            'temperature_moyenne': sum(d.temperature_moy or 0 for d in donnees) / len(donnees),
            'temperature_min': min(d.temperature_min or 999 for d in donnees),
            'temperature_max': max(d.temperature_max or -999 for d in donnees),
            'precipitation_totale': sum(d.precipitation or 0 for d in donnees),
            'jours_secheresse': len([d for d in donnees if d.stress_hydrique in ['modere', 'severe', 'extreme']]),
            'mois_plus_chaud': donnees.sorted('temperature_moy')[0].mois if donnees else None,
            'mois_plus_froid': donnees.sorted('temperature_moy', reverse=True)[0].mois if donnees else None
        }
        
        return stats
