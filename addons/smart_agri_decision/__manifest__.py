# -*- coding: utf-8 -*-
{
    'name': 'SmartAgriDecision',
    'version': '18.0.1.0.0',
    'category': 'Agriculture',
    'summary': 'Module d\'aide à la décision agricole basé sur l\'IA et les données spatiales',
    'description': """
        Module SmartAgriDecision pour Odoo 18
        =====================================
        
        Fonctionnalités principales :
        - Gestion des exploitations agricoles et parcelles
        - Intégration des données climatiques et météorologiques
        - Prédictions IA pour les rendements et recommandations
        - Tableaux de bord intelligents
        - Gestion des rotations culturales
        - Optimisation des ressources (eau, engrais, main-d'œuvre)
        - Simulation de scénarios climatiques
        - Alertes et recommandations en temps réel
        
        Technologies utilisées :
        - Odoo 18, PostgreSQL + PostGIS
        - Scikit-learn / XGBoost pour l'IA
        - Pandas pour l'analyse des données
        - Leaflet.js pour la cartographie
        - Intégration API météo et données sol
    """,
    'author': 'SmartAgri Team',
    'website': 'https://www.smartagri.com',
    'depends': [
        'base',
        'web',
        'mail',
        'base_geolocalize',
    ],
    'data': [
        # Données de base
        'data/sequences.xml',
        
        # Actions (AVANT les menus pour éviter les erreurs de références)
        'views/actions.xml',
        
        # Vues de base (sans références de menus)
        'views/soil_type_views.xml',
        'views/exploitation_views.xml',
        'views/parcelle_views.xml',
        'views/culture_views.xml',
        'views/meteo_views.xml',
        'views/intervention_views.xml',
        'views/intrants_views.xml',
        'views/utilisation_intrants_views.xml',
        'views/meteostat_import_views.xml',
        'views/alerte_climatique_views.xml',
        # TEMPORAIREMENT COMMENTÉ POUR RÉSOLUDRE L'ERREUR DE CHARGEMENT
        # 'views/alerte_exploitation_views.xml',
        'views/tendance_climatique_views.xml',
        'views/scenario_climatique_views.xml',
        'views/rcp_scenario_views.xml',
        'views/tableau_bord_views.xml',
        'views/rotation_culturelle_views.xml',
        'views/dashboard_views.xml',
        'views/geojson_wizard_views.xml',
        'views/assets.xml',
        
        # Vues IA (sans références de menus)
        'views/ia_predictions_views.xml',
        'views/ia_simulateur_views.xml',
        'views/ia_optimisation_ressources_views.xml',
        'views/ia_dashboard_views.xml',
        'views/ia_detection_stress_views.xml',
        'views/ai_model_views.xml',
        
        # Vues pour les stations météo (TEMPORAIREMENT COMMENTÉ)
        # 'views/station_meteo_views.xml',
        
        # Menu principal (AVANT tous les sous-menus)
        'views/main_menu.xml',
        
        # Menu principal unifié (plus de doublons)
        'views/menu_meteo_climat.xml',  # FICHIER TEMPORAIRE - Menu intégré dans main_menu.xml
        
        # SÉCURITÉ (APRÈS la création des modèles et vues)
        'security/ir.model.access.csv',
        
        # Données de démonstration marocaines (après la création des modèles et de la sécurité)
        'data/demo_data_maroc.xml',                # DONNÉES MAROCAINES PRINCIPALES
        'data/donnees_supplementaires.xml',
        'data/donnees_intenses.xml',
        'data/remplacement_odoo18_maroc.xml',      # REMPLACEMENT COMPLET ODOO 18 - MAROC
        'data/donnees_maroc_completes.xml',        # DONNÉES MAROCAINES COMPLÈTES
        'data/donnees_maroc_etendues.xml',         # DONNÉES MAROCAINES ÉTENDUES
        'data/donnees_ia_maroc_avancees.xml',      # DONNÉES IA MAROCAINES AVANCÉES
        'data/demo_data_complet.xml',              # FICHIER FANTÔME pour éviter l'erreur
        'data/demo_data_massive.xml',              # FICHIER FANTÔME pour éviter l'erreur
        'data/demo_data_complete.xml',             # FICHIER FANTÔME pour éviter l'erreur
        'data/demo_data_final.xml',                # FICHIER FANTÔME pour éviter l'erreur
    ],
    'demo': [
        'data/demo_data_maroc.xml',                # DONNÉES MAROCAINES PRINCIPALES
        'data/donnees_intenses.xml',
        'data/donnees_maroc_completes.xml',        # DONNÉES MAROCAINES COMPLÈTES
        'data/donnees_maroc_etendues.xml',         # DONNÉES MAROCAINES ÉTENDUES
        'data/donnees_ia_maroc_avancees.xml',      # DONNÉES IA MAROCAINES AVANCÉES
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
