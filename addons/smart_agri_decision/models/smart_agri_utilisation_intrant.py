# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SmartAgriUtilisationIntrant(models.Model):
    """Utilisation d'intrants agricoles"""

    _name = 'smart_agri_utilisation_intrant'
    _description = 'Utilisation d\'Intrants Agricoles'
    _order = 'date_utilisation desc'

    # RELATIONS PRINCIPALES - LOGIQUE MÉTIER
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True, ondelete='cascade')
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle', ondelete='cascade')
    intervention_id = fields.Many2one('smart_agri_intervention', string='Intervention', ondelete='cascade')
    intrant_id = fields.Many2one('smart_agri_intrants', string='Intrant', required=True, ondelete='cascade')

    # Champs de base
    name = fields.Char('Nom de l\'utilisation', required=True)
    description = fields.Text('Description de l\'utilisation')
    
    # Informations d'utilisation
    date_utilisation = fields.Date('Date d\'utilisation', required=True, default=fields.Date.today)
    quantite_utilisee = fields.Float('Quantité utilisée', required=True)
    unite_quantite = fields.Selection([
        ('kg', 'Kilogrammes'),
        ('l', 'Litres'),
        ('m3', 'Mètres cubes'),
        ('ha', 'Hectares'),
        ('unite', 'Unités')
    ], string='Unité de quantité', required=True, default='kg')
    
    # Coûts
    prix_unitaire = fields.Float('Prix unitaire', related='intrant_id.prix_unitaire', readonly=True)
    cout_utilisation = fields.Float('Coût total', compute='_compute_cout_utilisation', store=True)
    
    # Efficacité et résultats
    efficacite = fields.Selection([
        ('excellente', 'Excellente'),
        ('bonne', 'Bonne'),
        ('moyenne', 'Moyenne'),
        ('faible', 'Faible'),
        ('nulle', 'Nulle')
    ], string='Efficacité observée', default='moyenne')
    
    observations = fields.Text('Observations sur l\'efficacité')
    
    # Conditions d'application
    conditions_meteo = fields.Selection([
        ('ensoleille', 'Ensoleillé'),
        ('nuageux', 'Nuageux'),
        ('pluvieux', 'Pluvieux'),
        ('venteux', 'Venteux'),
        ('autre', 'Autre')
    ], string='Conditions météo')
    
    temperature_application = fields.Float('Température d\'application (°C)')
    humidite_application = fields.Float('Humidité d\'application (%)')
    
    # Statut
    state = fields.Selection([
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé')
    ], string='État', default='planifie')
    
    # Notes
    notes = fields.Text('Notes additionnelles')
    active = fields.Boolean('Actif', default=True)

    # Calcul du coût total
    @api.depends('quantite_utilisee', 'prix_unitaire')
    def _compute_cout_utilisation(self):
        for record in self:
            record.cout_utilisation = record.quantite_utilisee * record.prix_unitaire

    # Calcul automatique du nom
    @api.depends('intrant_id', 'parcelle_id', 'date_utilisation')
    def _compute_name(self):
        for record in self:
            if record.intrant_id and record.parcelle_id and record.date_utilisation:
                record.name = f"Utilisation {record.intrant_id.name} - {record.parcelle_id.name} - {record.date_utilisation.strftime('%d/%m/%Y')}"
            else:
                record.name = "Nouvelle utilisation d'intrant"

    # ONCHANGE pour mettre à jour les relations
    @api.onchange('intervention_id')
    def _onchange_intervention(self):
        if self.intervention_id:
            self.exploitation_id = self.intervention_id.exploitation_id
            self.parcelle_id = self.intervention_id.parcelle_id

    @api.onchange('parcelle_id')
    def _onchange_parcelle(self):
        if self.parcelle_id:
            self.exploitation_id = self.parcelle_id.exploitation_id

    # CONTRAINTES
    @api.constrains('quantite_utilisee')
    def _check_quantite_positive(self):
        for record in self:
            if record.quantite_utilisee <= 0:
                raise ValidationError('La quantité utilisée doit être strictement positive.')
    
    @api.constrains('date_utilisation')
    def _check_date_utilisation(self):
        for record in self:
            if record.date_utilisation > fields.Date.today():
                raise ValidationError('La date d\'utilisation ne peut pas être dans le futur.')

    # MÉTHODES MÉTIER
    def action_terminer_utilisation(self):
        """Marque l'utilisation comme terminée"""
        for record in self:
            record.state = 'termine'
    
    def action_annuler_utilisation(self):
        """Annule l'utilisation"""
        for record in self:
            record.state = 'annule'
    
    def action_planifier_utilisation(self):
        """Planifie l'utilisation"""
        for record in self:
            record.state = 'planifie'
