# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriMeteo(models.Model):
    """Données météorologiques"""

    _name = 'smart_agri_meteo'
    _description = 'Données Météorologiques'
    _order = 'date desc'

    # Champs de base
    name = fields.Char('Nom', compute='_compute_name', store=True)
    date = fields.Date('Date', required=True, default=fields.Date.today)
    
    # Données météo
    temperature_min = fields.Float('Température min (°C)')
    temperature_max = fields.Float('Température max (°C)')
    temperature_moyenne = fields.Float('Température moyenne (°C)')
    humidite = fields.Float('Humidité (%)')
    precipitation = fields.Float('Précipitations (mm)')
    ensoleillement = fields.Float('Ensoleillement (heures)')
    vitesse_vent = fields.Float('Vitesse du vent (km/h)')
    
    # Calcul automatique du nom
    @api.depends('date')
    def _compute_name(self):
        for record in self:
            if record.date:
                record.name = f"Météo du {record.date}"
            else:
                record.name = "Météo"
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes')
