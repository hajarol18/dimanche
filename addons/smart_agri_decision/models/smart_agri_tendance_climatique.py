# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SmartAgriTendanceClimatique(models.Model):
    """Tendances climatiques et analyses temporelles"""

    _name = 'smart_agri_tendance_climatique'
    _description = 'Tendance Climatique Agricole'
    _order = 'date_analyse desc'

    # RELATIONS PRINCIPALES
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True, ondelete='cascade')
    parcelle_id = fields.Many2one('smart_agri_parcelle', string='Parcelle', ondelete='cascade')
    
    # Champs de base
    name = fields.Char('Nom de l\'analyse', required=True)
    description = fields.Text('Description de l\'analyse')
    
    # Période d'analyse
    date_debut = fields.Date('Date de début', required=True)
    date_fin = fields.Date('Date de fin', required=True)
    date_analyse = fields.Date('Date d\'analyse', default=fields.Date.today)
    
    # Type d'analyse
    type_analyse = fields.Selection([
        ('temperature', '🌡️ Analyse des températures'),
        ('precipitation', '🌧️ Analyse des précipitations'),
        ('humidite', '💧 Analyse de l\'humidité'),
        ('vent', '💨 Analyse des vents'),
        ('stress_hydrique', '🌵 Stress hydrique'),
        ('indices_climatiques', '📊 Indices climatiques'),
        ('tendance_generale', '📈 Tendance générale'),
        ('autre', '🔍 Autre')
    ], string='Type d\'analyse', required=True)
    
    # Paramètres climatiques analysés
    temperature_moyenne = fields.Float('Température moyenne (°C)')
    temperature_min = fields.Float('Température minimale (°C)')
    temperature_max = fields.Float('Température maximale (°C)')
    precipitation_totale = fields.Float('Précipitations totales (mm)')
    humidite_moyenne = fields.Float('Humidité moyenne (%)')
    vitesse_vent_moyenne = fields.Float('Vitesse vent moyenne (km/h)')
    
    # Indices climatiques calculés
    indice_aridite = fields.Float('Indice d\'aridité', help='Rapport précipitations/évapotranspiration')
    indice_stress_hydrique = fields.Float('Indice de stress hydrique', help='0-100, 100 = stress maximal')
    indice_comfort_thermique = fields.Float('Indice de confort thermique', help='0-100, 100 = confort optimal')
    
    # Tendances calculées
    tendance_temperature = fields.Selection([
        ('hausse', '📈 Hausse'),
        ('baisse', '📉 Baisse'),
        ('stable', '➡️ Stable'),
        ('variable', '🔄 Variable')
    ], string='Tendance température')
    
    tendance_precipitation = fields.Selection([
        ('hausse', '📈 Hausse'),
        ('baisse', '📉 Baisse'),
        ('stable', '➡️ Stable'),
        ('variable', '🔄 Variable')
    ], string='Tendance précipitations')
    
    tendance_humidite = fields.Selection([
        ('hausse', '📈 Hausse'),
        ('baisse', '📉 Baisse'),
        ('stable', '➡️ Stable'),
        ('variable', '🔄 Variable')
    ], string='Tendance humidité')
    
    # Évolution des indices
    evolution_aridite = fields.Float('Évolution aridité (%)', help='Variation en pourcentage')
    evolution_stress_hydrique = fields.Float('Évolution stress hydrique (%)', help='Variation en pourcentage')
    evolution_comfort = fields.Float('Évolution confort (%)', help='Variation en pourcentage')
    
    # Recommandations
    recommandations = fields.Text('Recommandations basées sur l\'analyse')
    actions_prioritaires = fields.Text('Actions prioritaires')
    alertes_detectees = fields.Text('Alertes détectées')
    
    # Métadonnées
    source_donnees = fields.Selection([
        ('meteostat', 'Meteostat'),
        ('station_locale', 'Station locale'),
        ('api_meteo', 'API météo'),
        ('import_manuel', 'Import manuel'),
        ('autre', 'Autre')
    ], string='Source des données', required=True, default='meteostat')
    
    qualite_analyse = fields.Selection([
        ('excellente', 'Excellente'),
        ('bonne', 'Bonne'),
        ('moyenne', 'Moyenne'),
        ('faible', 'Faible')
    ], string='Qualité de l\'analyse', default='bonne')
    
    # Statut
    state = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('valide', 'Validé'),
        ('archive', 'Archivé')
    ], string='État', default='brouillon', required=True)
    
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes et observations')

    # MÉTHODES DE CALCUL DES TENDANCES
    @api.model
    def calculer_tendances_automatiques(self, exploitation_id, date_debut, date_fin):
        """Calcule automatiquement les tendances climatiques"""
        try:
            # Récupération des données météo
            donnees_meteo = self.env['smart_agri_meteo'].search([
                ('exploitation_id', '=', exploitation_id),
                ('date_mesure', '>=', date_debut),
                ('date_mesure', '<=', date_fin)
            ])
            
            if not donnees_meteo:
                return False
            
            # Calculs des moyennes
            temperatures = donnees_meteo.mapped('temperature')
            precipitations = donnees_meteo.mapped('precipitation')
            humidites = donnees_meteo.mapped('humidite')
            
            temp_moy = sum(temperatures) / len(temperatures) if temperatures else 0
            prec_tot = sum(precipitations) if precipitations else 0
            hum_moy = sum(humidites) / len(humidites) if humidites else 0
            
            # Calcul des tendances (simplifié)
            tendance_temp = 'stable'
            if len(temperatures) > 1:
                if temperatures[-1] > temperatures[0] * 1.1:
                    tendance_temp = 'hausse'
                elif temperatures[-1] < temperatures[0] * 0.9:
                    tendance_temp = 'baisse'
            
            tendance_prec = 'stable'
            if len(precipitations) > 1:
                if precipitations[-1] > precipitations[0] * 1.2:
                    tendance_prec = 'hausse'
                elif precipitations[-1] < precipitations[0] * 0.8:
                    tendance_prec = 'baisse'
            
            # Calcul des indices
            indice_aridite = (prec_tot / 30) / (temp_moy / 10) if temp_moy > 0 else 0
            indice_stress = max(0, 100 - (prec_tot / 10)) if prec_tot < 50 else 0
            indice_comfort = 100 - abs(temp_moy - 22) * 2 if 15 <= temp_moy <= 30 else 50
            
            return {
                'temperature_moyenne': round(temp_moy, 1),
                'precipitation_totale': round(prec_tot, 1),
                'humidite_moyenne': round(hum_moy, 1),
                'tendance_temperature': tendance_temp,
                'tendance_precipitation': tendance_prec,
                'indice_aridite': round(indice_aridite, 2),
                'indice_stress_hydrique': round(indice_stress, 1),
                'indice_comfort_thermique': round(indice_comfort, 1)
            }
            
        except Exception as e:
            _logger.error(f"Erreur calcul tendances: {str(e)}")
            return False

    def action_lancer_analyse(self):
        """Lance l'analyse des tendances climatiques"""
        self.ensure_one()
        
        if not self.date_debut or not self.date_fin:
            raise ValidationError("Les dates de début et fin sont obligatoires.")
        
        # Calcul automatique
        resultats = self.calculer_tendances_automatiques(
            self.exploitation_id.id, 
            self.date_debut, 
            self.date_fin
        )
        
        if resultats:
            self.write({
                'state': 'en_cours',
                **resultats
            })
            
            # Génération des recommandations
            recommandations = self._generer_recommandations(resultats)
            self.write({
                'recommandations': recommandations,
                'state': 'termine'
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Analyse terminée !',
                    'message': f'L\'analyse des tendances climatiques a été calculée avec succès.',
                    'type': 'success',
                }
            }
        else:
            raise ValidationError("Impossible de calculer les tendances. Vérifiez les données météo disponibles.")

    def _generer_recommandations(self, resultats):
        """Génère des recommandations basées sur l'analyse"""
        recommandations = []
        
        if resultats.get('tendance_temperature') == 'hausse':
            recommandations.append("🌡️ Hausse des températures détectée - Surveiller le stress thermique des cultures")
        
        if resultats.get('tendance_precipitation') == 'baisse':
            recommandations.append("🌵 Diminution des précipitations - Planifier l'irrigation d'appoint")
        
        if resultats.get('indice_stress_hydrique', 0) > 70:
            recommandations.append("🚨 Stress hydrique élevé - Actions d'urgence recommandées")
        
        if resultats.get('indice_comfort_thermique', 0) < 50:
            recommandations.append("⚠️ Conditions thermiques défavorables - Adapter les pratiques culturales")
        
        return "\n".join(recommandations) if recommandations else "✅ Conditions climatiques normales détectées."

    # CONTRAINTES
    @api.constrains('date_debut', 'date_fin')
    def _check_dates(self):
        """Vérifie la cohérence des dates"""
        for record in self:
            if record.date_debut and record.date_fin:
                if record.date_debut > record.date_fin:
                    raise ValidationError('La date de début doit être antérieure à la date de fin.')