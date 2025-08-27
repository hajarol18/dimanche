# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SmartAgriMeteo(models.Model):
    """Données météorologiques agricoles"""

    _name = 'smart_agri_meteo'
    _description = 'Données Météorologiques Agricoles'
    _order = 'date_mesure desc'

    # RELATIONS PRINCIPALES - LOGIQUE MÉTIER
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True, ondelete='cascade')
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle', ondelete='cascade')
    scenario_id = fields.Many2one('smart_agri_scenario_climatique', string='Scénario climatique', ondelete='set null')
    
    # Champs de base
    name = fields.Char('Nom de la mesure', required=True)
    description = fields.Text('Description de la mesure')
    
    # Informations temporelles
    date_mesure = fields.Date('Date de mesure', required=True, default=fields.Date.today)
    heure_mesure = fields.Float('Heure de mesure (format 24h)', default=12.0)
    
    # Données météorologiques principales
    temperature = fields.Float('Température (°C)', required=True)
    temperature_min = fields.Float('Température minimale (°C)')
    temperature_max = fields.Float('Température maximale (°C)')
    
    # Précipitations et humidité
    precipitation = fields.Float('Précipitations (mm)', default=0.0)
    humidite = fields.Float('Humidité relative (%)', default=0.0)
    
    # Vent et pression
    vitesse_vent = fields.Float('Vitesse du vent (km/h)', default=0.0)
    direction_vent = fields.Selection([
        ('nord', 'Nord'),
        ('nord_est', 'Nord-Est'),
        ('est', 'Est'),
        ('sud_est', 'Sud-Est'),
        ('sud', 'Sud'),
        ('sud_ouest', 'Sud-Ouest'),
        ('ouest', 'Ouest'),
        ('nord_ouest', 'Nord-Ouest')
    ], string='Direction du vent')
    
    pression_atmospherique = fields.Float('Pression atmosphérique (hPa)', default=1013.25)
    
    # Rayonnement solaire
    rayonnement_solaire = fields.Float('Rayonnement solaire (W/m²)', default=0.0)
    duree_ensoleillement = fields.Float('Durée d\'ensoleillement (heures)', default=0.0)
    
    # Source des données
    source = fields.Selection([
        ('station_locale', 'Station locale'),
        ('meteostat', 'Meteostat'),
        ('meteo_france', 'Météo France'),
        ('autre', 'Autre')
    ], string='Source des données', required=True, default='station_locale')
    
    # Qualité des données
    qualite_donnees = fields.Selection([
        ('excellente', 'Excellente'),
        ('bonne', 'Bonne'),
        ('moyenne', 'Moyenne'),
        ('faible', 'Faible')
    ], string='Qualité des données', default='bonne')
    
    # Notes et observations
    observations = fields.Text('Observations météorologiques')
    notes = fields.Text('Notes additionnelles')
    
    # Statut
    active = fields.Boolean('Actif', default=True)

    # Calcul automatique du nom
    @api.depends('date_mesure', 'temperature', 'exploitation_id')
    def _compute_name(self):
        for record in self:
            if record.date_mesure and record.exploitation_id:
                record.name = f"Météo {record.exploitation_id.name} - {record.date_mesure.strftime('%d/%m/%Y')} - {record.temperature}°C"
            elif record.date_mesure:
                record.name = f"Météo - {record.date_mesure.strftime('%d/%m/%Y')} - {record.temperature}°C"
            else:
                record.name = "Nouvelle mesure météo"

    # ONCHANGE pour mettre à jour les relations
    @api.onchange('parcelle_id')
    def _onchange_parcelle(self):
        """Met à jour l'exploitation quand la parcelle change"""
        if self.parcelle_id:
            self.exploitation_id = self.parcelle_id.exploitation_id

    # CONTRAINTES MÉTIER
    @api.constrains('date_mesure')
    def _check_date_mesure(self):
        """Vérifie que la date de mesure n'est pas dans le futur"""
        for record in self:
            if record.date_mesure > fields.Date.today():
                raise ValidationError('La date de mesure ne peut pas être dans le futur.')
    
    @api.constrains('temperature_min', 'temperature_max')
    def _check_temperature_coherence(self):
        """Vérifie la cohérence des températures min/max"""
        for record in self:
            if record.temperature_min and record.temperature_max:
                if record.temperature_min > record.temperature_max:
                    raise ValidationError('La température minimale ne peut pas être supérieure à la maximale.')
    
    @api.constrains('humidite')
    def _check_humidite_range(self):
        """Vérifie que l'humidité est dans une plage valide"""
        for record in self:
            if record.humidite < 0 or record.humidite > 100:
                raise ValidationError('L\'humidité doit être comprise entre 0% et 100%.')

    # MÉTHODES MÉTIER
    def action_voir_exploitation(self):
        """Action pour voir l'exploitation associée"""
        return {
            'name': f'Exploitation {self.exploitation_id.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_exploitation',
            'view_mode': 'form',
            'res_id': self.exploitation_id.id,
        }
    
    def action_voir_parcelle(self):
        """Action pour voir la parcelle associée"""
        if self.parcelle_id:
            return {
                'name': f'Parcelle {self.parcelle_id.name}',
                'type': 'ir.actions.act_window',
                'res_model': 'smart_agri_parcelle',
                'view_mode': 'form',
                'res_id': self.parcelle_id.id,
            }
    
    def action_analyser_tendances(self):
        """Action pour analyser les tendances météorologiques"""
        return {
            'name': f'Analyse des tendances météo - {self.exploitation_id.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_tendance_climatique',
            'view_mode': 'list,form',
            'domain': [('exploitation_id', '=', self.exploitation_id.id)],
            'context': {'default_exploitation_id': self.exploitation_id.id},
        }
