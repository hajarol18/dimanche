# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SmartAgriRcpScenario(models.Model):
    """Scénarios climatiques IPCC RCP (Representative Concentration Pathways)"""

    _name = 'smart_agri_rcp_scenario'
    _description = 'Scénario Climatique IPCC RCP'
    _order = 'code_rcp'

    # CODE RCP - LES 4 SCÉNARIOS DU CAHIER DES CHARGES
    code_rcp = fields.Selection([
        ('rcp_2_6', 'RCP 2.6 - Optimiste (Limitation du réchauffement à +2°C)'),
        ('rcp_4_5', 'RCP 4.5 - Intermédiaire (Réduction modérée des émissions)'),
        ('rcp_6_0', 'RCP 6.0 - Intermédiaire-Haut (Stabilisation des émissions)'),
        ('rcp_8_5', 'RCP 8.5 - Pessimiste (Émissions continues élevées)')
    ], string='Code RCP', required=True)
    
    # Nom et description
    name = fields.Char('Nom du scénario', required=True)
    description = fields.Text('Description détaillée du scénario')
    
    # Caractéristiques climatiques
    rechauffement_2030 = fields.Float('Réchauffement 2030 (+°C)', help='Réchauffement prévu d\'ici 2030')
    rechauffement_2050 = fields.Float('Réchauffement 2050 (+°C)', help='Réchauffement prévu d\'ici 2050')
    rechauffement_2100 = fields.Float('Réchauffement 2100 (+°C)', help='Réchauffement prévu d\'ici 2100')
    
    # Émissions de CO2
    emissions_2030 = fields.Float('Émissions CO2 2030 (Gt/an)', help='Émissions de CO2 prévues en 2030')
    emissions_2050 = fields.Float('Émissions CO2 2050 (Gt/an)', help='Émissions de CO2 prévues en 2050')
    emissions_2100 = fields.Float('Émissions CO2 2100 (Gt/an)', help='Émissions de CO2 prévues en 2100')
    
    # Impacts agricoles prévus
    impact_secheresse = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('critique', 'Critique')
    ], string='Impact Sécheresse', required=True)
    
    impact_precipitation = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('critique', 'Critique')
    ], string='Impact Précipitations', required=True)
    
    impact_temperature = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('critique', 'Critique')
    ], string='Impact Température', required=True)
    
    # Probabilité d'occurrence
    probabilite_occurrence = fields.Float('Probabilité d\'occurrence (%)', help='Probabilité que ce scénario se réalise')
    
    # Source des données
    source_donnees = fields.Char('Source des données', default='IPCC AR6')
    date_mise_a_jour = fields.Date('Date de mise à jour', default=fields.Date.today)
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    notes = fields.Text('Notes additionnelles')

    # CHAMPS CALCULÉS
    niveau_risque = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('critique', 'Critique')
    ], string='Niveau de Risque Global', compute='_compute_niveau_risque', store=True)
    
    score_impact = fields.Float('Score d\'Impact', compute='_compute_score_impact', store=True)
    
    @api.depends('impact_secheresse', 'impact_precipitation', 'impact_temperature')
    def _compute_niveau_risque(self):
        """Calcule le niveau de risque global basé sur les impacts"""
        for record in self:
            impacts = [record.impact_secheresse, record.impact_precipitation, record.impact_temperature]
            
            if 'critique' in impacts:
                record.niveau_risque = 'critique'
            elif 'eleve' in impacts:
                record.niveau_risque = 'eleve'
            elif 'modere' in impacts:
                record.niveau_risque = 'modere'
            else:
                record.niveau_risque = 'faible'
    
    @api.depends('impact_secheresse', 'impact_precipitation', 'impact_temperature', 'probabilite_occurrence')
    def _compute_score_impact(self):
        """Calcule un score d'impact numérique"""
        for record in self:
            # Conversion des impacts en scores numériques
            impact_scores = {
                'faible': 1,
                'modere': 2,
                'eleve': 3,
                'critique': 4
            }
            
            score = (impact_scores.get(record.impact_secheresse, 0) + 
                    impact_scores.get(record.impact_precipitation, 0) + 
                    impact_scores.get(record.impact_temperature, 0)) / 3
            
            # Pondération par la probabilité
            record.score_impact = score * (record.probabilite_occurrence / 100)

    # MÉTHODES MÉTIER
    def action_analyser_impacts(self):
        """Action pour analyser les impacts de ce scénario RCP"""
        return {
            'name': f'Analyse Impacts - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_scenario_climatique',
            'view_mode': 'list,form',
            'domain': [('rcp_scenario_id', '=', self.id)],
            'context': {'default_rcp_scenario_id': self.id},
        }

    def action_voir_tendances(self):
        """Action pour voir les tendances liées à ce scénario"""
        return {
            'name': f'Tendances - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_tendance_climatique',
            'view_mode': 'list,form',
            'domain': [('rcp_scenario_id', '=', self.id)],
            'context': {'default_rcp_scenario_id': self.id},
        }

    def action_simuler_scenario(self):
        """Action pour simuler ce scénario climatique"""
        return {
            'name': f'Simulation - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_scenario_climatique',
            'view_mode': 'form',
            'context': {
                'default_rcp_scenario_id': self.id,
                'default_name': f'Simulation {self.name}',
                'default_description': f'Simulation basée sur le scénario {self.name}'
            },
        }

    # CONTRAINTES
    @api.constrains('probabilite_occurrence')
    def _check_probabilite_range(self):
        """Vérifie que la probabilité est dans une plage valide"""
        for record in self:
            if record.probabilite_occurrence < 0 or record.probabilite_occurrence > 100:
                raise ValidationError('La probabilité d\'occurrence doit être comprise entre 0% et 100%.')

    @api.constrains('rechauffement_2030', 'rechauffement_2050', 'rechauffement_2100')
    def _check_progression_rechauffement(self):
        """Vérifie la progression logique du réchauffement"""
        for record in self:
            if (record.rechauffement_2030 is not False and record.rechauffement_2050 is not False and 
                record.rechauffement_2030 > record.rechauffement_2050):
                raise ValidationError('Le réchauffement 2030 ne peut pas être supérieur à celui de 2050.')
            
            if (record.rechauffement_2050 is not False and record.rechauffement_2100 is not False and 
                record.rechauffement_2050 > record.rechauffement_2100):
                raise ValidationError('Le réchauffement 2050 ne peut pas être supérieur à celui de 2100.')

    @api.constrains('code_rcp')
    def _check_code_rcp_unique(self):
        """Vérifie que le code RCP est unique"""
        for record in self:
            if record.code_rcp:
                existing = self.search([('code_rcp', '=', record.code_rcp), ('id', '!=', record.id)])
                if existing:
                    raise ValidationError(f'Le code RCP {record.code_rcp} existe déjà.')

    # MÉTHODES DE CRÉATION AUTOMATIQUE
    @api.model
    def creer_scenarios_rcp_par_defaut(self):
        """Crée automatiquement les 4 scénarios RCP IPCC"""
        scenarios_data = [
            {
                'code_rcp': 'rcp_2_6',
                'name': 'RCP 2.6 - Optimiste',
                'description': 'Scénario optimiste avec limitation du réchauffement à +2°C d\'ici 2100',
                'rechauffement_2030': 1.5,
                'rechauffement_2050': 2.0,
                'rechauffement_2100': 2.0,
                'emissions_2030': 30.0,
                'emissions_2050': 15.0,
                'emissions_2100': 5.0,
                'impact_secheresse': 'faible',
                'impact_precipitation': 'faible',
                'impact_temperature': 'faible',
                'probabilite_occurrence': 20.0
            },
            {
                'code_rcp': 'rcp_4_5',
                'name': 'RCP 4.5 - Intermédiaire',
                'description': 'Scénario intermédiaire avec réduction modérée des émissions',
                'rechauffement_2030': 1.8,
                'rechauffement_2050': 2.5,
                'rechauffement_2100': 3.0,
                'emissions_2030': 35.0,
                'emissions_2050': 25.0,
                'emissions_2100': 15.0,
                'impact_secheresse': 'modere',
                'impact_precipitation': 'modere',
                'impact_temperature': 'modere',
                'probabilite_occurrence': 35.0
            },
            {
                'code_rcp': 'rcp_6_0',
                'name': 'RCP 6.0 - Intermédiaire-Haut',
                'description': 'Scénario intermédiaire-haut avec stabilisation des émissions',
                'rechauffement_2030': 2.0,
                'rechauffement_2050': 3.0,
                'rechauffement_2100': 4.0,
                'emissions_2030': 40.0,
                'emissions_2050': 35.0,
                'emissions_2100': 25.0,
                'impact_secheresse': 'eleve',
                'impact_precipitation': 'eleve',
                'impact_temperature': 'eleve',
                'probabilite_occurrence': 25.0
            },
            {
                'code_rcp': 'rcp_8_5',
                'name': 'RCP 8.5 - Pessimiste',
                'description': 'Scénario pessimiste avec émissions continues élevées',
                'rechauffement_2030': 2.5,
                'rechauffement_2050': 4.0,
                'rechauffement_2100': 6.0,
                'emissions_2030': 45.0,
                'emissions_2050': 50.0,
                'emissions_2100': 45.0,
                'impact_secheresse': 'critique',
                'impact_precipitation': 'critique',
                'impact_temperature': 'critique',
                'probabilite_occurrence': 20.0
            }
        ]
        
        for scenario_data in scenarios_data:
            existing = self.search([('code_rcp', '=', scenario_data['code_rcp'])])
            if not existing:
                self.create(scenario_data)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Scénarios RCP créés !',
                'message': 'Les 4 scénarios RCP IPCC ont été créés avec succès !',
                'type': 'success',
            }
        }
