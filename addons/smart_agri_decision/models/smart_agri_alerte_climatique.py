# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class SmartAgriAlerteClimatique(models.Model):
    """Alertes climatiques automatiques selon le cahier des charges"""

    _name = 'smart_agri_alerte_climatique'
    _description = 'Alerte Climatique Agricole'
    _order = 'date_detection desc, niveau desc'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # RELATION PRINCIPALE
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True, ondelete='cascade')
    
    # Champs de base
    name = fields.Char('Nom de l\'alerte', required=True)
    description = fields.Text('Description détaillée de l\'alerte')
    
    # Type d'alerte selon cahier des charges
    type_alerte = fields.Selection([
        ('secheresse', '🌵 Sécheresse'),
        ('gel', '❄️ Gel'),
        ('canicule', '🔥 Canicule'),
        ('inondation', '🌊 Inondation'),
        ('vent_fort', '💨 Vent fort'),
        ('grele', '🧊 Grêle'),
        ('autre', '⚠️ Autre')
    ], string='Type d\'alerte', required=True)
    
    # Niveau de gravité
    niveau = fields.Selection([
        ('vert', '🟢 Normal'),
        ('jaune', '🟡 Attention'),
        ('orange', '🟠 Alerte'),
        ('rouge', '🔴 Danger'),
        ('noir', '⚫ Extrême')
    ], string='Niveau de gravité', required=True, default='jaune')
    
    # Dates
    date_detection = fields.Date('Date de détection', required=True, default=fields.Date.today)
    date_debut = fields.Date('Date de début de l\'événement')
    date_fin = fields.Date('Date de fin de l\'événement')
    
    # Source de l'alerte
    source = fields.Selection([
        ('import_meteo', '🌤️ Import Météo Automatique'),
        ('api_meteo', '🌍 API Météo Externe'),
        ('capteur_local', '📡 Capteur Local'),
        ('utilisateur', '👤 Saisie Utilisateur'),
        ('ia_prediction', '🧠 Prédiction IA'),
        ('autre', '📊 Autre')
    ], string='Source de l\'alerte', required=True, default='import_meteo')
    
    # Paramètres météorologiques déclencheurs
    temperature_min = fields.Float('Température minimale (°C)')
    temperature_max = fields.Float('Température maximale (°C)')
    precipitation = fields.Float('Précipitations (mm)')
    humidite = fields.Float('Humidité (%)')
    vent_vitesse = fields.Float('Vitesse du vent (km/h)')
    
    # Impact agricole
    impact_cultures = fields.Many2many('smart_agri_culture', string='Cultures impactées')
    impact_parcelles = fields.Many2many('smart_agri_parcelle', string='Parcelles impactées')
    niveau_impact = fields.Selection([
        ('faible', '🟢 Faible'),
        ('modere', '🟡 Modéré'),
        ('eleve', '🟠 Élevé'),
        ('critique', '🔴 Critique'),
        ('catastrophique', '⚫ Catastrophique')
    ], string='Niveau d\'impact agricole', default='modere')
    
    # Actions recommandées
    actions_recommandees = fields.Text('Actions recommandées')
    actions_urgentes = fields.Text('Actions urgentes à effectuer')
    
    # Statut de l'alerte
    state = fields.Selection([
        ('active', '🚨 Active'),
        ('surveillee', '👁️ Surveillée'),
        ('resolue', '✅ Résolue'),
        ('fausse_alerte', '❌ Fausse alerte'),
        ('archivée', '📁 Archivée')
    ], string='État de l\'alerte', default='active')
    
    # Notifications
    notifiee = fields.Boolean('Alerte notifiée', default=False)
    date_notification = fields.Datetime('Date de notification')
    
    # Notes et commentaires
    notes = fields.Text('Notes et commentaires')
    
    # Priorité de traitement
    priorite = fields.Selection([
        ('basse', '🟢 Basse'),
        ('normale', '🟡 Normale'),
        ('haute', '🟠 Haute'),
        ('urgente', '🔴 Urgente'),
        ('critique', '⚫ Critique')
    ], string='Priorité de traitement', compute='_compute_priorite', store=True)
    
    # Statut
    active = fields.Boolean('Actif', default=True)
    
    # Calcul automatique de la priorité
    @api.depends('niveau', 'type_alerte', 'niveau_impact')
    def _compute_priorite(self):
        """Calcule automatiquement la priorité de traitement"""
        for record in self:
            # Priorité basée sur le niveau et le type d'alerte
            if record.niveau in ['noir', 'rouge']:
                record.priorite = 'critique'
            elif record.niveau == 'orange':
                record.priorite = 'urgente'
            elif record.niveau == 'jaune':
                record.priorite = 'haute'
            else:
                record.priorite = 'normale'
            
            # Ajuster selon le type d'alerte
            if record.type_alerte in ['gel', 'grele']:
                record.priorite = 'urgente' if record.priorite == 'haute' else record.priorite
            elif record.type_alerte == 'secheresse' and record.niveau_impact in ['eleve', 'critique']:
                record.priorite = 'urgente' if record.priorite == 'haute' else record.priorite

    # Méthode pour notifier l'alerte
    def notifier_alerte(self):
        """Notifie l'alerte aux utilisateurs concernés"""
        for record in self:
            if not record.notifiee:
                record.notifiee = True
                record.date_notification = fields.Datetime.now()
                
                # Création d'un message dans le système de messagerie Odoo
                try:
                    record.message_post(
                        body=f"Alerte climatique {record.type_alerte} - Niveau {record.niveau} détectée pour l'exploitation {record.exploitation_id.name}",
                        subject=f"🚨 Alerte Climatique: {record.name}",
                        message_type='notification'
                    )
                except Exception as e:
                    # Fallback si message_post échoue
                    _logger.warning(f"Impossible de poster le message: {e}")
                
                # Log de la notification
                _logger.info(f"Alerte climatique notifiée: {record.name} pour {record.exploitation_id.name}")

    # Méthode pour résoudre l'alerte
    def resoudre_alerte(self):
        """Marque l'alerte comme résolue"""
        for record in self:
            record.state = 'resolue'
            record.date_fin = fields.Date.today()

    # Méthode pour archiver l'alerte
    def archiver_alerte(self):
        """Archive l'alerte"""
        for record in self:
            record.state = 'archivée'
            record.active = False

    # Méthode pour créer des alertes automatiques selon les données météo
    @api.model
    def creer_alerte_automatique(self, exploitation_id, type_alerte, niveau, description, source='import_meteo'):
        """Crée automatiquement une alerte climatique"""
        return self.create({
            'name': f'Alerte {type_alerte} - {exploitation_id.name}',
            'exploitation_id': exploitation_id.id,
            'type_alerte': type_alerte,
            'niveau': niveau,
            'description': description,
            'source': source,
            'date_detection': fields.Date.today(),
            'state': 'active'
        })

    # Contraintes de validation
    @api.constrains('date_debut', 'date_fin')
    def _check_dates_alerte(self):
        """Vérifie la cohérence des dates d'alerte"""
        for record in self:
            if record.date_debut and record.date_fin:
                if record.date_debut > record.date_fin:
                    raise ValidationError(_("La date de début doit être antérieure à la date de fin."))

    @api.constrains('temperature_min', 'temperature_max')
    def _check_temperatures(self):
        """Vérifie la cohérence des températures"""
        for record in self:
            if record.temperature_min and record.temperature_max:
                if record.temperature_min > record.temperature_max:
                    raise ValidationError(_("La température minimale doit être inférieure à la température maximale."))

    @api.constrains('humidite')
    def _check_humidite(self):
        """Vérifie la validité de l'humidité"""
        for record in self:
            if record.humidite and (record.humidite < 0 or record.humidite > 100):
                raise ValidationError(_("L'humidité doit être comprise entre 0 et 100%."))

    # Méthode pour générer des recommandations automatiques
    def generer_recommandations(self):
        """Génère automatiquement des recommandations selon le type d'alerte"""
        for record in self:
            if record.type_alerte == 'secheresse':
                record.actions_recommandees = """
                🌱 Actions recommandées en cas de sécheresse:
                • Augmenter la fréquence d'irrigation
                • Utiliser des techniques de paillage
                • Surveiller l'état hydrique des sols
                • Adapter les cultures à la sécheresse
                """
                record.actions_urgentes = """
                🚨 Actions urgentes:
                • Vérifier les systèmes d'irrigation
                • Réduire les pertes d'eau
                • Planifier l'irrigation d'urgence
                """
                
            elif record.type_alerte == 'gel':
                record.actions_recommandees = """
                ❄️ Actions recommandées en cas de gel:
                • Protéger les cultures sensibles
                • Utiliser des voiles de protection
                • Surveiller les prévisions météo
                • Retarder les plantations si possible
                """
                record.actions_urgentes = """
                🚨 Actions urgentes:
                • Installer les protections anti-gel
                • Vérifier les systèmes de chauffage
                • Préparer les plans d'urgence
                """
                
            elif record.type_alerte == 'canicule':
                record.actions_recommandees = """
                🔥 Actions recommandées en cas de canicule:
                • Augmenter l'irrigation
                • Protéger du soleil intense
                • Surveiller le stress hydrique
                • Adapter les horaires de travail
                """
                record.actions_urgentes = """
                🚨 Actions urgentes:
                • Irrigation d'urgence
                • Protection des cultures sensibles
                • Surveillance renforcée
                """

    # Méthode pour analyser l'impact sur les cultures
    def analyser_impact_cultures(self):
        """Analyse l'impact de l'alerte sur les cultures de l'exploitation"""
        for record in self:
            if record.exploitation_id:
                # Récupérer les cultures actives
                cultures_actives = self.env['smart_agri_culture'].search([
                    ('exploitation_id', '=', record.exploitation_id.id),
                    ('state', '=', 'active')
                ])
                
                if cultures_actives:
                    record.impact_cultures = [(6, 0, cultures_actives.ids)]
                    
                    # Analyser la vulnérabilité selon le type d'alerte
                    cultures_vulnerables = []
                    for culture in cultures_actives:
                        if record.type_alerte == 'secheresse' and culture.famille in ['cereales', 'legumes']:
                            cultures_vulnerables.append(culture.id)
                        elif record.type_alerte == 'gel' and culture.famille in ['fruits', 'legumes_precoces']:
                            cultures_vulnerables.append(culture.id)
                        elif record.type_alerte == 'canicule' and culture.famille in ['legumes', 'fruits']:
                            cultures_vulnerables.append(culture.id)
                    
                    if cultures_vulnerables:
                        record.impact_cultures = [(6, 0, cultures_vulnerables)]
                        record.niveau_impact = 'eleve'
                    else:
                        record.niveau_impact = 'modere'
