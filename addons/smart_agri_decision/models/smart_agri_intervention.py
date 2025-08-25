# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriIntervention(models.Model):
    """Intervention agricole - Planification complète"""

    _name = 'smart_agri_intervention'
    _description = 'Intervention Agricole'
    _order = 'date_planifiee'

    # Champs de base
    name = fields.Char('Nom de l\'intervention', required=True)
    description = fields.Text('Description détaillée')
    
    # Références aux autres modèles
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True)
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle')
    culture_id = fields.Many2one('smart_agri_culture', string='Culture concernée')
    
    # Type d'intervention détaillé
    type_intervention = fields.Selection([
        ('semis', 'Semis'),
        ('irrigation', 'Irrigation'),
        ('traitement', 'Traitement phytosanitaire'),
        ('recolte', 'Récolte'),
        ('fertilisation', 'Fertilisation'),
        ('labour', 'Labour'),
        ('desherbage', 'Désherbage'),
        ('taille', 'Taille'),
        ('greffage', 'Greffage'),
        ('autre', 'Autre')
    ], string='Type d\'intervention', required=True)
    
    # Planification temporelle
    date_planifiee = fields.Date('Date planifiée', required=True)
    date_execution = fields.Date('Date d\'exécution')
    duree_estimee = fields.Float('Durée estimée (heures)', default=1.0)
    
    # Statut et suivi
    state = fields.Selection([
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
        ('retardee', 'Retardée')
    ], string='État', default='planifiee')
    
    # Ressources et coûts
    main_oeuvre_requise = fields.Float('Main d\'œuvre requise (heures)')
    cout_estime = fields.Float('Coût estimé (€)')
    cout_reel = fields.Float('Coût réel (€)')
    
    # Conditions météorologiques
    conditions_meteo = fields.Text('Conditions météo requises')
    temperature_min = fields.Float('Température minimum (°C)')
    temperature_max = fields.Float('Température maximum (°C)')
    humidite_min = fields.Float('Humidité minimum (%)')
    
    # Notes et observations
    notes = fields.Text('Notes et observations')
    resultats = fields.Text('Résultats obtenus')
    problemes_rencontres = fields.Text('Problèmes rencontrés')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    
    # Calcul automatique du nom
    @api.depends('type_intervention', 'parcelle_id', 'date_planifiee')
    def _compute_name(self):
        for record in self:
            if record.type_intervention and record.parcelle_id and record.date_planifiee:
                record.name = f"{record.type_intervention.title()} - {record.parcelle_id.name} - {record.date_planifiee}"
            elif record.type_intervention:
                record.name = f"{record.type_intervention.title()} - {record.date_planifiee}"
            else:
                record.name = "Nouvelle intervention"
