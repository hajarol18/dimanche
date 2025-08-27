# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class SmartAgriMeteostatImport(models.Model):
    """Import automatique des données Meteostat"""

    _name = 'smart_agri_meteostat_import'
    _description = 'Import Meteostat Automatique'
    _order = 'date_import desc'

    # RELATION PRINCIPALE - LOGIQUE MÉTIER
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True, ondelete='cascade')

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
    @api.depends('station_id', 'date_debut', 'date_fin', 'exploitation_id')
    def _compute_name(self):
        for record in self:
            if record.exploitation_id and record.station_id and record.date_debut and record.date_fin:
                record.name = f"Import Meteostat {record.exploitation_id.name} - {record.station_id} - {record.date_debut.strftime('%d/%m/%Y')} à {record.date_fin.strftime('%d/%m/%Y')}"
            elif record.station_id and record.date_debut and record.date_fin:
                record.name = f"Import Meteostat {record.station_id} - {record.date_debut.strftime('%d/%m/%Y')} à {record.date_fin.strftime('%d/%m/%Y')}"
            else:
                record.name = "Nouvel import Meteostat"

    # ONCHANGE pour mettre à jour les coordonnées depuis l'exploitation
    @api.onchange('exploitation_id')
    def _onchange_exploitation(self):
        """Met à jour les coordonnées depuis l'exploitation"""
        if self.exploitation_id:
            # On pourrait récupérer les coordonnées de l'exploitation
            # Pour l'instant, on laisse l'utilisateur les saisir
            pass

    # Méthode d'import Meteostat simplifiée
    def importer_donnees_meteostat(self):
        """Import des données depuis Meteostat (version simplifiée)"""
        for record in self:
            try:
                record.state = 'en_cours'
                record.nombre_enregistrements = 0
                record.erreur_import = ''
                
                # Simulation d'import réussi
                record.nombre_enregistrements = 10
                record.state = 'termine'
                record.duree_import = 5.0
                record.log_import = 'Import simulé avec succès'
                
            except Exception as e:
                record.state = 'erreur'
                record.erreur_import = str(e)
                record.log_import = f'Erreur lors de l\'import: {str(e)}'

    # Méthode pour créer des enregistrements météo simulés
    def _creer_enregistrements_meteo(self):
        """Crée des enregistrements météo simulés"""
        MeteoModel = self.env['smart_agri_meteo']
        
        for record in self:
            if record.state == 'termine':
                # Créer quelques enregistrements météo simulés
                for i in range(record.nombre_enregistrements):
                    date_mesure = record.date_debut + timedelta(days=i)
                    MeteoModel.create({
                        'exploitation_id': record.exploitation_id.id,
                        'date_mesure': date_mesure,
                        'temperature': 20.0 + (i % 10),
                        'precipitation': (i % 3) * 5.0,
                        'humidite': 60.0 + (i % 20),
                        'source': 'Meteostat (simulé)'
                    })
