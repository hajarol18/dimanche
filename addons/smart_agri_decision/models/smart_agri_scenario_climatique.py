# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SmartAgriScenarioClimatique(models.Model):
    """Scénarios climatiques personnalisés pour simulations"""

    _name = 'smart_agri_scenario_climatique'
    _description = 'Scénario Climatique Agricole'
    _order = 'name'

    # RELATIONS PRINCIPALES
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', ondelete='cascade')
    
    # Champs de base
    name = fields.Char('Nom du scénario', required=True)
    description = fields.Text('Description du scénario')
    code = fields.Char('Code scénario', required=True, size=20)
    
    # Type de scénario
    type_scenario = fields.Selection([
        ('secheresse', '🌵 Scénario Sécheresse'),
        ('pluie_abondante', '🌧️ Scénario Pluie Abondante'),
        ('canicule', '🔥 Scénario Canicule'),
        ('hiver_rigoureux', '❄️ Scénario Hiver Rigoureux'),
        ('mousson_tardive', '🌦️ Scénario Mousson Tardive'),
        ('vent_fort', '💨 Scénario Vent Fort'),
        ('variabilite_climatique', '🔄 Variabilité Climatique'),
        ('rechauffement_global', '🌍 Réchauffement Global'),
        ('refroidissement', '🧊 Refroidissement'),
        ('personnalise', '⚙️ Scénario Personnalisé'),
        ('autre', '🔍 Autre')
    ], string='Type de scénario', required=True)
    
    # Période du scénario
    date_debut = fields.Date('Date de début', required=True)
    date_fin = fields.Date('Date de fin', required=True)
    duree_jours = fields.Integer('Durée (jours)', compute='_compute_duree', store=True)
    
    # Paramètres climatiques du scénario
    temperature_base = fields.Float('Température de base (°C)', default=20.0)
    variation_temperature = fields.Float('Variation température (°C)', default=0.0, 
                                       help='Variation par rapport à la normale')
    temperature_min = fields.Float('Température minimale (°C)')
    temperature_max = fields.Float('Température maximale (°C)')
    
    precipitation_base = fields.Float('Précipitations de base (mm)', default=0.0)
    variation_precipitation = fields.Float('Variation précipitations (%)', default=0.0,
                                         help='Variation en pourcentage par rapport à la normale')
    precipitation_min = fields.Float('Précipitations minimales (mm)')
    precipitation_max = fields.Float('Précipitations maximales (mm)')
    
    humidite_base = fields.Float('Humidité de base (%)', default=60.0)
    variation_humidite = fields.Float('Variation humidité (%)', default=0.0)
    humidite_min = fields.Float('Humidité minimale (%)')
    humidite_max = fields.Float('Humidité maximale (%)')
    
    vent_base = fields.Float('Vent de base (km/h)', default=10.0)
    variation_vent = fields.Float('Variation vent (km/h)', default=0.0)
    vent_min = fields.Float('Vent minimal (km/h)')
    vent_max = fields.Float('Vent maximal (km/h)')
    
    # Intensité du scénario
    intensite = fields.Selection([
        ('faible', '🟢 Faible'),
        ('moderee', '🟡 Modérée'),
        ('forte', '🟠 Forte'),
        ('extreme', '🔴 Extrême'),
        ('catastrophique', '⚫ Catastrophique')
    ], string='Intensité', required=True, default='moderee')
    
    # Probabilité d'occurrence
    probabilite_occurrence = fields.Selection([
        ('tres_faible', 'Très faible (0-20%)'),
        ('faible', 'Faible (20-40%)'),
        ('moyenne', 'Moyenne (40-60%)'),
        ('elevee', 'Élevée (60-80%)'),
        ('tres_elevee', 'Très élevée (80-100%)')
    ], string='Probabilité d\'occurrence', default='moyenne')
    
    # Impact agricole prévu
    impact_rendement = fields.Float('Impact sur rendement (%)', default=0.0,
                                  help='Variation du rendement en pourcentage')
    impact_qualite = fields.Selection([
        ('amelioration', 'Amélioration'),
        ('stable', 'Stable'),
        ('degradation_legere', 'Dégradation légère'),
        ('degradation_moderee', 'Dégradation modérée'),
        ('degradation_severe', 'Dégradation sévère')
    ], string='Impact sur la qualité', default='stable')
    
    # Cultures affectées
    cultures_affectees = fields.Many2many('smart_agri_culture', string='Cultures affectées')
    parcelles_affectees = fields.Many2many('smart_agri_parcelle', string='Parcelles affectées')
    
    # Mesures d'adaptation recommandées
    mesures_adaptation = fields.Text('Mesures d\'adaptation recommandées')
    actions_preventives = fields.Text('Actions préventives')
    actions_curatives = fields.Text('Actions curatives')
    
    # Simulation et résultats
    simulation_lancee = fields.Boolean('Simulation lancée', default=False)
    date_simulation = fields.Datetime('Date de simulation')
    resultats_simulation = fields.Text('Résultats de la simulation')
    
    # Statut
    state = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('valide', 'Validé'),
        ('simulation_en_cours', 'Simulation en cours'),
        ('simulation_terminee', 'Simulation terminée'),
        ('archive', 'Archivé')
    ], string='État', default='brouillon', required=True)
    
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes et observations')

    @api.depends('date_debut', 'date_fin')
    def _compute_duree(self):
        """Calcule la durée du scénario en jours"""
        for record in self:
            if record.date_debut and record.date_fin:
                delta = record.date_fin - record.date_debut
                record.duree_jours = delta.days + 1
            else:
                record.duree_jours = 0

    @api.model_create_multi
    def create(self, vals_list):
        """Génération automatique du code scénario"""
        for vals in vals_list:
            if not vals.get('code'):
                name = vals.get('name', 'SCEN')
                code = name.upper().replace(' ', '_')[:15]
                counter = 1
                while self.search_count([('code', '=', code)]) > 0:
                    code = f"{name.upper().replace(' ', '_')[:12]}_{counter:03d}"
                    counter += 1
                vals['code'] = code
        return super().create(vals_list)

    def action_lancer_simulation(self):
        """Lance la simulation du scénario climatique"""
        self.ensure_one()
        
        if not self.exploitation_id:
            raise ValidationError("Une exploitation doit être sélectionnée pour la simulation.")
        
        try:
            # Mise à jour du statut
            self.write({
                'state': 'simulation_en_cours',
                'simulation_lancee': True,
                'date_simulation': fields.Datetime.now()
            })
            
            # Simulation des impacts
            resultats = self._simuler_impacts()
            
            # Mise à jour des résultats
            self.write({
                'resultats_simulation': resultats,
                'state': 'simulation_terminee'
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Simulation terminée !',
                    'message': f'La simulation du scénario {self.name} a été lancée avec succès.',
                    'type': 'success',
                }
            }
            
        except Exception as e:
            _logger.error(f"Erreur simulation scénario: {str(e)}")
            self.write({'state': 'brouillon'})
            raise ValidationError(f"Erreur lors de la simulation: {str(e)}")

    def _simuler_impacts(self):
        """Simule les impacts du scénario climatique"""
        resultats = []
        
        # Analyse de l'intensité
        if self.intensite == 'extreme':
            impact_rendement = -30
        elif self.intensite == 'forte':
            impact_rendement = -15
        elif self.intensite == 'moderee':
            impact_rendement = -5
        elif self.intensite == 'faible':
            impact_rendement = 0
        else:  # catastrophique
            impact_rendement = -50
        
        # Ajustement selon le type de scénario
        if self.type_scenario == 'secheresse':
            impact_rendement -= 20
            resultats.append("🌵 Sécheresse: Impact sévère sur les cultures non irriguées")
        elif self.type_scenario == 'canicule':
            impact_rendement -= 15
            resultats.append("🔥 Canicule: Stress thermique des cultures")
        elif self.type_scenario == 'pluie_abondante':
            impact_rendement -= 10
            resultats.append("🌧️ Pluie abondante: Risque de maladies fongiques")
        elif self.type_scenario == 'hiver_rigoureux':
            impact_rendement -= 25
            resultats.append("❄️ Hiver rigoureux: Risque de gel des cultures sensibles")
        
        # Calcul final de l'impact
        impact_final = impact_rendement + self.impact_rendement
        resultats.append(f"📊 Impact sur le rendement: {impact_final:.1f}%")
        
        # Recommandations
        if impact_final < -20:
            resultats.append("🚨 Actions d'urgence recommandées")
        elif impact_final < -10:
            resultats.append("⚠️ Mesures préventives nécessaires")
        else:
            resultats.append("✅ Impact limité, surveillance recommandée")
        
        return "\n".join(resultats)

    def action_generer_alertes(self):
        """Génère des alertes basées sur le scénario"""
        self.ensure_one()
        
        if not self.exploitation_id:
            return
        
        # Création d'alertes selon le scénario
        alerte_data = {
            'name': f'Alerte Scénario: {self.name}',
            'exploitation_id': self.exploitation_id.id,
            'type_alerte': self._get_type_alerte(),
            'niveau': self._get_niveau_alerte(),
            'severite': self.intensite,
            'description': f'Scénario climatique: {self.description}',
            'source': 'scenario_climatique',
            'type_source': 'scenario_rcp'
        }
        
        alerte = self.env['smart_agri_alerte_climatique'].create(alerte_data)
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_alerte_climatique',
            'res_id': alerte.id,
            'view_mode': 'form',
            'target': 'current'
        }

    def _get_type_alerte(self):
        """Retourne le type d'alerte selon le scénario"""
        mapping = {
            'secheresse': 'secheresse',
            'canicule': 'canicule',
            'pluie_abondante': 'inondation',
            'hiver_rigoureux': 'gel',
            'vent_fort': 'vent_fort',
            'grele': 'grele'
        }
        return mapping.get(self.type_scenario, 'autre')

    def _get_niveau_alerte(self):
        """Retourne le niveau d'alerte selon l'intensité"""
        mapping = {
            'faible': 'jaune',
            'moderee': 'orange',
            'forte': 'rouge',
            'extreme': 'rouge',
            'catastrophique': 'noir'
        }
        return mapping.get(self.intensite, 'jaune')

    # CONTRAINTES
    @api.constrains('date_debut', 'date_fin')
    def _check_dates(self):
        """Vérifie la cohérence des dates"""
        for record in self:
            if record.date_debut and record.date_fin:
                if record.date_debut > record.date_fin:
                    raise ValidationError('La date de début doit être antérieure à la date de fin.')
    
    @api.constrains('variation_temperature', 'variation_precipitation', 'variation_humidite')
    def _check_variations(self):
        """Vérifie la cohérence des variations"""
        for record in self:
            if abs(record.variation_temperature) > 50:
                raise ValidationError('La variation de température doit être comprise entre -50°C et +50°C.')
            if abs(record.variation_precipitation) > 500:
                raise ValidationError('La variation de précipitations doit être comprise entre -500% et +500%.')
            if abs(record.variation_humidite) > 100:
                raise ValidationError('La variation d\'humidité doit être comprise entre -100% et +100%.')