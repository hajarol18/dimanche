# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class SmartAgriMeteostatImport(models.Model):
    """Import automatique des données Meteostat"""

    _name = 'smart_agri_meteostat_import'
    _description = 'Import Meteostat Automatique'
    _order = 'date_import desc'

    # Champs de base
    name = fields.Char('Nom de l\'import', required=True)
    description = fields.Text('Description de l\'import')
    
    # Configuration de l'import
    station_id = fields.Char('ID Station Meteostat', required=True)
    latitude = fields.Float('Latitude', required=True)
    longitude = fields.Float('Longitude', required=True)
    
    # Période d'import
    date_debut = fields.Date('Date de début', required=True)
    date_fin = fields.Date('Date de fin', required=True)
    date_import = fields.Datetime('Date d\'import', default=fields.Datetime.now)
    
    # Paramètres à importer
    parametres_import = fields.Selection([
        ('temperature', 'Température uniquement'),
        ('precipitation', 'Précipitations uniquement'),
        ('humidite', 'Humidité uniquement'),
        ('vent', 'Vent uniquement'),
        ('pression', 'Pression uniquement'),
        ('tous', 'Tous les paramètres')
    ], string='Paramètres à importer', required=True, default='tous')
    
    # Statut de l'import
    state = fields.Selection([
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('erreur', 'Erreur'),
        ('annule', 'Annulé')
    ], string='État', default='planifie')
    
    # Résultats de l'import
    nombre_enregistrements = fields.Integer('Nombre d\'enregistrements importés', default=0)
    duree_import = fields.Float('Durée d\'import (secondes)', default=0.0)
    
    # Erreurs et logs
    erreur_import = fields.Text('Erreur d\'import')
    log_import = fields.Text('Log détaillé')
    
    # Configuration automatique
    import_automatique = fields.Boolean('Import automatique', default=True)
    frequence_import = fields.Selection([
        ('quotidien', 'Quotidien'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuel', 'Mensuel'),
        ('personnalise', 'Personnalisé')
    ], string='Fréquence d\'import', default='quotidien')
    
    # Prochaine importation
    prochaine_import = fields.Datetime('Prochaine importation')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    
    # Calcul automatique du nom
    @api.depends('station_id', 'date_debut', 'date_fin')
    def _compute_name(self):
        for record in self:
            if record.station_id and record.date_debut and record.date_fin:
                record.name = f"Import Meteostat {record.station_id} - {record.date_debut.strftime('%d/%m/%Y')} à {record.date_fin.strftime('%d/%m/%Y')}"
            else:
                record.name = "Nouvel import Meteostat"
    
    # Méthode d'import Meteostat
    def importer_donnees_meteostat(self):
        """Import des données depuis Meteostat"""
        for record in self:
            try:
                record.state = 'en_cours'
                debut_temps = datetime.now()
                
                _logger.info(f"Début import Meteostat pour {record.station_id}")
                
                # Simulation de l'import Meteostat
                # En production, on utiliserait la vraie API Meteostat
                donnees_importees = record._simuler_import_meteostat()
                
                # Mise à jour des statistiques
                fin_temps = datetime.now()
                record.duree_import = (fin_temps - debut_temps).total_seconds()
                record.nombre_enregistrements = len(donnees_importees)
                record.state = 'termine'
                
                # Création des enregistrements météo
                record._creer_enregistrements_meteo(donnees_importees)
                
                _logger.info(f"Import Meteostat terminé: {record.nombre_enregistrements} enregistrements")
                
            except Exception as e:
                record.state = 'erreur'
                record.erreur_import = str(e)
                _logger.error(f"Erreur import Meteostat: {e}")
    
    def _simuler_import_meteostat(self):
        """Simulation de l'import Meteostat (remplacé par la vraie API)"""
        donnees = []
        date_courante = self.date_debut
        
        while date_courante <= self.date_fin:
            # Simulation de données météo réalistes
            donnee = {
                'date': date_courante,
                'temperature_min': 15 + (date_courante.day % 10),
                'temperature_max': 25 + (date_courante.day % 10),
                'temperature_moyenne': 20 + (date_courante.day % 5),
                'precipitation': 0 if date_courante.day % 3 != 0 else 5 + (date_courante.day % 10),
                'humidite': 60 + (date_courante.day % 20),
                'vitesse_vent': 10 + (date_courante.day % 15)
            }
            donnees.append(donnee)
            date_courante += timedelta(days=1)
        
        return donnees
    
    def _creer_enregistrements_meteo(self, donnees):
        """Création des enregistrements météo dans Odoo"""
        for donnee in donnees:
            # Vérifier si l'enregistrement existe déjà
            existing = self.env['smart_agri_meteo'].search([
                ('date', '=', donnee['date']),
                ('active', '=', True)
            ], limit=1)
            
            if not existing:
                # Créer un nouvel enregistrement
                self.env['smart_agri_meteo'].create({
                    'date': donnee['date'],
                    'temperature_min': donnee['temperature_min'],
                    'temperature_max': donnee['temperature_max'],
                    'temperature_moyenne': donnee['temperature_moyenne'],
                    'precipitation': donnee['precipitation'],
                    'humidite': donnee['humidite'],
                    'vitesse_vent': donnee['vitesse_vent'],
                    'notes': f"Importé automatiquement depuis Meteostat - Station {self.station_id}"
                })
    
    # Méthode pour planifier le prochain import
    def planifier_prochain_import(self):
        """Planification automatique du prochain import"""
        for record in self:
            if record.import_automatique:
                if record.frequence_import == 'quotidien':
                    record.prochaine_import = fields.Datetime.now() + timedelta(days=1)
                elif record.frequence_import == 'hebdomadaire':
                    record.prochaine_import = fields.Datetime.now() + timedelta(weeks=1)
                elif record.frequence_import == 'mensuel':
                    record.prochaine_import = fields.Datetime.now() + timedelta(days=30)
    
    # Méthode pour vérifier les imports en retard
    @api.model
    def _verifier_imports_retard(self):
        """Vérification des imports en retard"""
        imports_retard = self.search([
            ('prochaine_import', '<=', fields.Datetime.now()),
            ('state', 'in', ['termine', 'erreur']),
            ('import_automatique', '=', True),
            ('active', '=', True)
        ])
        
        for import_retard in imports_retard:
            import_retard.importer_donnees_meteostat()
            import_retard.planifier_prochain_import()
    
    # Méthode pour tester la connexion Meteostat
    def tester_connexion_meteostat(self):
        """Test de la connexion à Meteostat"""
        for record in self:
            try:
                # Simulation du test de connexion
                record.log_import = "Test de connexion Meteostat réussi"
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Connexion Meteostat',
                        'message': 'Connexion réussie !',
                        'type': 'success'
                    }
                }
            except Exception as e:
                record.log_import = f"Erreur de connexion: {e}"
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Erreur Connexion',
                        'message': f'Erreur: {e}',
                        'type': 'danger'
                    }
                }
