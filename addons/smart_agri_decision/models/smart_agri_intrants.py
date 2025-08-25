# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriIntrants(models.Model):
    """Intrants agricoles - Suivi complet des ressources"""

    _name = 'smart_agri_intrants'
    _description = 'Intrants Agricoles'
    _order = 'name'

    # Champs de base
    name = fields.Char('Nom de l\'intrant', required=True)
    code = fields.Char('Code produit', required=True, size=20)
    description = fields.Text('Description détaillée')
    
    # Type d'intrant détaillé
    type_intrant = fields.Selection([
        ('semences', 'Semences'),
        ('plants', 'Plants'),
        ('engrais', 'Engrais'),
        ('pesticides', 'Pesticides'),
        ('herbicides', 'Herbicides'),
        ('fongicides', 'Fongicides'),
        ('insecticides', 'Insecticides'),
        ('eau', 'Eau d\'irrigation'),
        ('amendements', 'Amendements organiques'),
        ('substrats', 'Substrats de culture'),
        ('autre', 'Autre')
    ], string='Type d\'intrant', required=True)
    
    # Caractéristiques techniques
    unite = fields.Char('Unité de mesure', required=True)
    prix_unitaire = fields.Float('Prix unitaire (€)', required=True)
    stock_disponible = fields.Float('Stock disponible', default=0.0)
    stock_minimum = fields.Float('Stock minimum d\'alerte', default=0.0)
    
    # Qualité et certification
    qualite = fields.Selection([
        ('bio', 'Biologique'),
        ('conventionnel', 'Conventionnel'),
        ('hve', 'Haute Valeur Environnementale'),
        ('autre', 'Autre')
    ], string='Qualité', default='conventionnel')
    
    # Fournisseur et traçabilité
    fournisseur = fields.Char('Fournisseur')
    numero_lot = fields.Char('Numéro de lot')
    date_fabrication = fields.Date('Date de fabrication')
    date_peremption = fields.Date('Date de péremption')
    
    # Utilisation et suivi
    utilisation_ids = fields.One2many('smart_agri_utilisation_intrant', 'intrant_id', string='Utilisations')
    cout_total = fields.Float('Coût total d\'utilisation', compute='_compute_cout_total', store=True)
    
    # Impact environnemental
    impact_environnemental = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé')
    ], string='Impact environnemental', default='modere')
    
    # Notes et documentation
    notes = fields.Text('Notes et observations')
    documentation = fields.Binary('Documentation technique')
    nom_fichier_doc = fields.Char('Nom du fichier')
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    
    # Calcul du coût total
    @api.depends('utilisation_ids.cout_utilisation')
    def _compute_cout_total(self):
        for record in self:
            record.cout_total = sum(record.utilisation_ids.mapped('cout_utilisation'))
    
    # Alerte de stock
    @api.model
    def _check_stock_alert(self):
        intrants_alert = self.search([
            ('stock_disponible', '<=', 'stock_minimum'),
            ('active', '=', True)
        ])
        return intrants_alert


class SmartAgriUtilisationIntrant(models.Model):
    """Utilisation des intrants - Traçabilité complète"""
    
    _name = 'smart_agri_utilisation_intrant'
    _description = 'Utilisation des Intrants'
    _order = 'date_utilisation desc'
    
    # Références
    intrant_id = fields.Many2one('smart_agri_intrants', string='Intrant', required=True)
    intervention_id = fields.Many2one('smart_agri_intervention', string='Intervention')
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle')
    
    # Utilisation
    date_utilisation = fields.Date('Date d\'utilisation', required=True, default=fields.Date.today)
    quantite_utilisee = fields.Float('Quantité utilisée', required=True)
    unite_utilisation = fields.Char('Unité', related='intrant_id.unite', readonly=True)
    
    # Coûts
    cout_unitaire = fields.Float('Coût unitaire (€)', related='intrant_id.prix_unitaire', readonly=True)
    cout_utilisation = fields.Float('Coût total (€)', compute='_compute_cout_utilisation', store=True)
    
    # Conditions d'application
    conditions_meteo = fields.Text('Conditions météo lors de l\'application')
    temperature_application = fields.Float('Température lors de l\'application (°C)')
    humidite_application = fields.Float('Humidité lors de l\'application (%)')
    
    # Efficacité et résultats
    efficacite = fields.Selection([
        ('excellente', 'Excellente'),
        ('bonne', 'Bonne'),
        ('moyenne', 'Moyenne'),
        ('faible', 'Faible'),
        ('nulle', 'Nulle')
    ], string='Efficacité observée')
    
    observations = fields.Text('Observations et résultats')
    
    # Calcul du coût total
    @api.depends('quantite_utilisee', 'cout_unitaire')
    def _compute_cout_utilisation(self):
        for record in self:
            record.cout_utilisation = record.quantite_utilisee * record.cout_unitaire
