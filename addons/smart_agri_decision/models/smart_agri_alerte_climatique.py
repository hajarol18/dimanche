# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class SmartAgriAlerteClimatique(models.Model):
    """Alertes climatiques agricoles"""

    _name = 'smart_agri_alerte_climatique'
    _description = 'Alertes Climatiques Agricoles'
    _order = 'date_alerte desc'

    # Champs de base
    name = fields.Char('Nom de l\'alerte', required=True)
    description = fields.Text('Description détaillée')
    
    # Type d'alerte selon le cahier des charges
    type_alerte = fields.Selection([
        ('secheresse', 'Sécheresse'),
        ('gel', 'Gel'),
        ('canicule', 'Canicule'),
        ('pluies_intenses', 'Pluies intenses'),
        ('vent_fort', 'Vent fort'),
        ('grele', 'Grêle'),
        ('inondation', 'Inondation'),
        ('autre', 'Autre')
    ], string='Type d\'alerte', required=True)
    
    # Niveau de gravité
    niveau_gravite = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('critique', 'Critique')
    ], string='Niveau de gravité', required=True, default='modere')
    
    # Dates et durée
    date_alerte = fields.Datetime('Date de l\'alerte', required=True, default=fields.Datetime.now)
    date_debut = fields.Date('Date de début', required=True)
    date_fin = fields.Date('Date de fin estimée')
    duree_estimee = fields.Integer('Durée estimée (jours)', compute='_compute_duree', store=True)
    
    # Zone géographique
    zone_geographique = fields.Char('Zone géographique concernée')
    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')
    rayon_impact = fields.Float('Rayon d\'impact (km)', default=10.0)
    
    # Données météorologiques
    temperature_min = fields.Float('Température minimum (°C)')
    temperature_max = fields.Float('Température maximum (°C)')
    precipitation = fields.Float('Précipitations (mm)')
    humidite = fields.Float('Humidité (%)')
    vitesse_vent = fields.Float('Vitesse du vent (km/h)')
    
    # Impact agricole
    impact_cultures = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('catastrophique', 'Catastrophique')
    ], string='Impact sur les cultures', default='modere')
    
    cultures_menacees = fields.Text('Cultures menacées')
    parcelles_concernées = fields.Text('Parcelles concernées')
    
    # Recommandations
    recommandations = fields.Text('Recommandations pour les agriculteurs')
    mesures_prevention = fields.Text('Mesures de prévention')
    actions_urgence = fields.Text('Actions d\'urgence')
    
    # Statut et suivi
    state = fields.Selection([
        ('active', 'Active'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée')
    ], string='État', default='active')
    
    # Source de l'alerte
    source_alerte = fields.Selection([
        ('api_meteo', 'API Météo'),
        ('meteo_france', 'Météo France'),
        ('agriculteur', 'Signalement agriculteur'),
        ('capteur_local', 'Capteur local'),
        ('autre', 'Autre')
    ], string='Source de l\'alerte', required=True)
    
    # Notifications
    notifiee = fields.Boolean('Alerte notifiée', default=False)
    date_notification = fields.Datetime('Date de notification')
    
    # Notes et documentation
    notes = fields.Text('Notes et observations')
    documentation = fields.Binary('Documentation associée')
    nom_fichier_doc = fields.Char('Nom du fichier')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    
    # Calcul automatique de la durée
    @api.depends('date_debut', 'date_fin')
    def _compute_duree(self):
        for record in self:
            if record.date_debut and record.date_fin:
                delta = record.date_fin - record.date_debut
                record.duree_estimee = delta.days
            else:
                record.duree_estimee = 0
    
    # Calcul automatique du nom
    @api.depends('type_alerte', 'niveau_gravite', 'date_alerte')
    def _compute_name(self):
        for record in self:
            if record.type_alerte and record.niveau_gravite and record.date_alerte:
                record.name = f"Alerte {record.type_alerte.title()} - {record.niveau_gravite.title()} - {record.date_alerte.strftime('%d/%m/%Y')}"
            else:
                record.name = "Nouvelle alerte climatique"
    
    # Méthode pour vérifier les alertes actives
    @api.model
    def _check_active_alerts(self):
        active_alerts = self.search([
            ('state', '=', 'active'),
            ('date_fin', '>=', fields.Date.today())
        ])
        return active_alerts
    
    # Méthode pour notifier les agriculteurs
    def notifier_agriculteurs(self):
        for record in self:
            if not record.notifiee:
                record.notifiee = True
                record.date_notification = fields.Datetime.now()
                # Ici on pourrait ajouter la logique d'envoi d'emails/SMS
