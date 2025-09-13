# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class SmartAgriIntrants(models.Model):
    """Intrants agricoles - Suivi complet des ressources avec IA"""

    _name = 'smart_agri_intrants'
    _description = 'Intrants Agricoles Intelligents'
    _order = 'name'
    _rec_name = 'name'

    # RELATION PRINCIPALE - LOGIQUE MÉTIER
    exploitation_id = fields.Many2one('smart_agri_exploitation', string='Exploitation', required=True, ondelete='cascade')

    # Champs de base
    name = fields.Char('Nom de l\'intrant', required=True)
    code = fields.Char('Code produit', size=20, copy=False, readonly=True)
    description = fields.Text('Description détaillée')
    
    # Type d'intrant simplifié pour une meilleure UX
    categorie_principale = fields.Selection([
        ('semences_plants', '🌱 Semences et Plants'),
        ('fertilisants', '🌿 Fertilisants'),
        ('protection_plantes', '🛡️ Protection des Plantes'),
        ('irrigation', '💧 Irrigation'),
        ('amendements', '🌾 Amendements'),
        ('equipements', '🔧 Équipements'),
        ('autre', '📦 Autre')
    ], string='Catégorie principale', required=True, default='fertilisants')
    
    type_intrant = fields.Selection([
        # Semences et Plants
        ('semences', '🌱 Semences'),
        ('plants', '🌿 Plants'),
        ('bulbes', '🌷 Bulbes'),
        ('greffons', '🌳 Greffons'),
        
        # Fertilisants - Simplifié
        ('engrais_azote', '🌿 Engrais azoté'),
        ('engrais_phosphore', '🌿 Engrais phosphaté'),
        ('engrais_potassium', '🌿 Engrais potassique'),
        ('engrais_complexe', '🌿 Engrais complexe'),
        ('engrais_organique', '🌿 Engrais organique'),
        
        # Protection des Plantes - Simplifié
        ('herbicide', '🛡️ Herbicide'),
        ('fongicide', '🛡️ Fongicide'),
        ('insecticide', '🛡️ Insecticide'),
        ('biocontrole', '🛡️ Biocontrôle'),
        
        # Irrigation
        ('eau_irrigation', '💧 Eau d\'irrigation'),
        ('systeme_irrigation', '💧 Système d\'irrigation'),
        
        # Amendements - Simplifié
        ('compost', '🌾 Compost'),
        ('fumier', '🌾 Fumier'),
        ('substrat', '🌾 Substrat'),
        
        # Équipements - Simplifié
        ('outil_manuel', '🔧 Outil manuel'),
        ('machine', '🔧 Machine'),
        ('protection_personnelle', '🔧 Protection'),
        
        ('autre', '📦 Autre')
    ], string='Type d\'intrant', required=True, default='engrais_complexe')
    
    # Caractéristiques techniques simplifiées
    unite = fields.Selection([
        ('kg', 'Kilogrammes (kg)'),
        ('l', 'Litres (l)'),
        ('m3', 'Mètres cubes (m³)'),
        ('ha', 'Hectares (ha)'),
        ('unite', 'Unités'),
        ('tonne', 'Tonnes (t)')
    ], string='Unité de mesure', required=True, default='kg')
    prix_unitaire = fields.Float('Prix unitaire (€)', digits=(10, 2))
    stock_disponible = fields.Float('Stock disponible', default=0.0, digits=(10, 2))
    stock_minimum = fields.Float('Stock minimum d\'alerte', default=0.0, digits=(10, 2))
    stock_maximum = fields.Float('Stock maximum recommandé', digits=(10, 2))
    
    # Champs calculés avancés
    cout_total = fields.Float('Coût total (€)', compute='_compute_cout_total', store=True, digits=(12, 2))
    valeur_stock = fields.Float('Valeur du stock (€)', compute='_compute_valeur_stock', store=True, digits=(12, 2))
    niveau_stock = fields.Selection([
        ('critique', 'Critique'),
        ('faible', 'Faible'),
        ('normal', 'Normal'),
        ('eleve', 'Élevé'),
        ('excessif', 'Excessif')
    ], string='Niveau de stock', compute='_compute_niveau_stock', store=True)
    
    # Qualité et certification avancées
    qualite = fields.Selection([
        ('bio', 'Biologique'),
        ('conventionnel', 'Conventionnel'),
        ('hve', 'Haute Valeur Environnementale'),
        ('demeter', 'Demeter'),
        ('nature_progres', 'Nature & Progrès'),
        ('autre', 'Autre')
    ], string='Qualité', default='conventionnel')
    
    certification_bio = fields.Boolean('Certification biologique')
    numero_certification = fields.Char('Numéro de certification')
    date_certification = fields.Date('Date de certification')
    
    # Fournisseur et traçabilité avancées
    fournisseur = fields.Char('Fournisseur')
    fournisseur_id = fields.Many2one('res.partner', string='Fournisseur (Contact)')
    numero_lot = fields.Char('Numéro de lot')
    numero_commande = fields.Char('Numéro de commande')
    date_fabrication = fields.Date('Date de fabrication')
    date_peremption = fields.Date('Date de péremption')
    duree_vie_utile = fields.Integer('Durée de vie utile (mois)')
    
    # Impact environnemental et sécurité
    impact_environnemental = fields.Selection([
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('critique', 'Critique')
    ], string='Impact environnemental', default='modere')
    
    classe_toxicite = fields.Selection([
        ('non_classifie', 'Non classifié'),
        ('faible', 'Faible'),
        ('modere', 'Modéré'),
        ('eleve', 'Élevé'),
        ('tres_eleve', 'Très élevé')
    ], string='Classe de toxicité', default='non_classifie')
    
    # Caractéristiques agronomiques
    composition = fields.Text('Composition détaillée')
    dosage_recommande = fields.Float('Dosage recommandé (kg/ha)')
    frequence_application = fields.Char('Fréquence d\'application')
    periode_application = fields.Text('Période d\'application recommandée')
    
    # Gestion des stocks et alertes
    alerte_stock = fields.Boolean('Alerte de stock activée', default=True)
    seuil_alerte_critique = fields.Float('Seuil d\'alerte critique', default=0.0)
    date_derniere_commande = fields.Date('Date de dernière commande')
    quantite_commande_habituelle = fields.Float('Quantité commandée habituellement')
    
    # Notes et documentation
    notes = fields.Text('Notes et observations')
    documentation = fields.Binary('Documentation technique')
    nom_fichier_doc = fields.Char('Nom du fichier')
    url_documentation = fields.Char('URL documentation')
    
    # Statut et suivi
    active = fields.Boolean('Actif', default=True)
    state = fields.Selection([
        ('disponible', 'Disponible'),
        ('en_rupture', 'En rupture'),
        ('en_commande', 'En commande'),
        ('perime', 'Périmé'),
        ('retire', 'Retiré du marché')
    ], string='État', default='disponible', compute='_compute_state', store=True)

    # ========================================
    # MÉTHODES DE CRÉATION AUTOMATIQUE
    # ========================================
    
    @api.model
    def create(self, vals):
        """Génère automatiquement le code si non fourni"""
        if not vals.get('code'):
            # Génère un code basé sur la catégorie et un numéro séquentiel
            categorie = vals.get('categorie_principale', 'autre')
            prefix = categorie[:3].upper()
            last_record = self.search([('code', 'like', prefix)], limit=1, order='code desc')
            if last_record and last_record.code:
                try:
                    last_num = int(last_record.code.split('-')[-1])
                    new_num = last_num + 1
                except:
                    new_num = 1
            else:
                new_num = 1
            vals['code'] = f"{prefix}-{new_num:04d}"
        return super().create(vals)

    # ========================================
    # CHAMPS CALCULÉS
    # ========================================
    
    @api.depends('prix_unitaire', 'stock_disponible')
    def _compute_cout_total(self):
        """Calcule le coût total de l'intrant"""
        for record in self:
            record.cout_total = record.prix_unitaire * record.stock_disponible
    
    @api.depends('prix_unitaire', 'stock_disponible')
    def _compute_valeur_stock(self):
        """Calcule la valeur totale du stock"""
        for record in self:
            record.valeur_stock = record.prix_unitaire * record.stock_disponible
    
    @api.depends('stock_disponible', 'stock_minimum', 'stock_maximum')
    def _compute_niveau_stock(self):
        """Détermine le niveau de stock"""
        for record in self:
            if record.stock_disponible <= record.seuil_alerte_critique:
                record.niveau_stock = 'critique'
            elif record.stock_disponible <= record.stock_minimum:
                record.niveau_stock = 'faible'
            elif record.stock_maximum and record.stock_disponible >= record.stock_maximum:
                record.niveau_stock = 'excessif'
            elif record.stock_disponible > record.stock_minimum * 1.5:
                record.niveau_stock = 'eleve'
            else:
                record.niveau_stock = 'normal'
    
    @api.depends('stock_disponible', 'stock_minimum', 'date_peremption')
    def _compute_state(self):
        """Détermine l'état de l'intrant"""
        for record in self:
            if record.stock_disponible <= 0:
                record.state = 'en_rupture'
            elif record.date_peremption and record.date_peremption < fields.Date.today():
                record.state = 'perime'
            else:
                record.state = 'disponible'

    # ========================================
    # MÉTHODES MÉTIER AVANCÉES
    # ========================================
    
    def action_voir_utilisations(self):
        """Action pour voir les utilisations de cet intrant"""
        return {
            'name': f'Utilisations de {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_utilisation_intrant',
            'view_mode': 'list,form',
            'domain': [('intrant_id', '=', self.id)],
            'context': {'default_intrant_id': self.id, 'default_exploitation_id': self.exploitation_id.id},
        }
    
    def action_ajuster_stock(self):
        """Action pour ajuster le stock de l'intrant"""
        return {
            'name': f'Ajuster le stock de {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_intrants',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            'context': {'default_action': 'ajuster_stock'}
        }
    
    def action_commander_intrant(self):
        """Action pour commander l'intrant"""
        return {
            'name': f'Commander {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_intrants',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            'context': {'default_action': 'commander'}
        }
    
    def action_analyser_utilisation(self):
        """Action pour analyser l'utilisation de l'intrant"""
        return {
            'name': f'Analyse d\'utilisation de {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'smart_agri_utilisation_intrant',
            'view_mode': 'graph,pivot,list',
            'domain': [('intrant_id', '=', self.id)],
            'context': {'default_intrant_id': self.id}
        }
    
    def action_generer_rapport_stock(self):
        """Génère un rapport de stock pour l'intrant"""
        return {
            'name': f'Rapport de stock - {self.name}',
            'type': 'ir.actions.report',
            'report_name': 'smart_agri_decision.report_intrant_stock',
            'report_type': 'qweb-pdf',
            'data': {'intrant_id': self.id}
        }
    
    # ========================================
    # MÉTHODES DE GESTION AUTOMATIQUE
    # ========================================
    
    def action_verifier_stock(self):
        """Vérifie automatiquement le niveau de stock et génère des alertes"""
        for record in self:
            if record.alerte_stock and record.niveau_stock in ['critique', 'faible']:
                record._generer_alerte_stock()
    
    def _generer_alerte_stock(self):
        """Génère une alerte de stock"""
        message = f"⚠️ ALERTE STOCK : {self.name} - Niveau : {self.niveau_stock}"
        if self.niveau_stock == 'critique':
            message += " - COMMANDE URGENTE REQUISE"
        
        # Ici on pourrait créer une alerte dans le système
        _logger.warning(f"Alerte stock pour {self.name}: {message}")
    
    def action_renouveler_stock(self):
        """Renouvelle automatiquement le stock selon les paramètres"""
        for record in self:
            if record.stock_disponible <= record.stock_minimum:
                quantite_a_commander = record.quantite_commande_habituelle or record.stock_maximum or 100
                record._creer_commande_automatique(quantite_a_commander)
    
    def _creer_commande_automatique(self, quantite):
        """Crée une commande automatique"""
        # Ici on pourrait créer une commande automatique
        _logger.info(f"Commande automatique créée pour {self.name}: {quantite} {self.unite}")
    
    # ========================================
    # CONTRAINTES ET VALIDATIONS
    # ========================================
    
    @api.constrains('stock_disponible', 'stock_minimum')
    def _check_stock_coherence(self):
        """Vérifie la cohérence des stocks"""
        for record in self:
            if record.stock_disponible < 0:
                raise ValidationError("Le stock disponible ne peut pas être négatif.")
            if record.stock_minimum < 0:
                raise ValidationError("Le stock minimum ne peut pas être négatif.")
    
    @api.constrains('prix_unitaire')
    def _check_prix_positif(self):
        """Vérifie que le prix est positif"""
        for record in self:
            if record.prix_unitaire <= 0:
                raise ValidationError("Le prix unitaire doit être strictement positif.")
    
    @api.constrains('date_fabrication', 'date_peremption')
    def _check_dates_coherence(self):
        """Vérifie la cohérence des dates"""
        for record in self:
            if record.date_fabrication and record.date_peremption:
                if record.date_fabrication >= record.date_peremption:
                    raise ValidationError("La date de fabrication doit être antérieure à la date de péremption.")
    
    # ========================================
    # MÉTHODES DE RECHERCHE AVANCÉES
    # ========================================
    
    @api.model
    def _search_intrants_critiques(self, operator, value):
        """Recherche les intrants en stock critique"""
        domain = [('niveau_stock', '=', 'critique')]
        return domain
    
    @api.model
    def _search_intrants_perimes(self, operator, value):
        """Recherche les intrants périmés"""
        domain = [('date_peremption', '<', fields.Date.today())]
        return domain
    
    @api.model
    def _search_intrants_bio(self, operator, value):
        """Recherche les intrants biologiques"""
        domain = [('qualite', '=', 'bio')]
        return domain
