{
    'name': 'Smart Agri Decision',
    'version': '1.0',
    'depends': [
        'base'
    ],
    'author': 'Hajar',
    'category': 'Agriculture',
    'summary': 'Module d\'aide à la décision agricole basé sur l\'IA et les données spatiales',
    'description': '''
Module d'aide à la décision agricole basé sur l\'IA et les données spatiales
==============================================

Ce module permet aux agriculteurs de :
- Gérer leurs exploitations et parcelles
- Analyser les données météorologiques
- Obtenir des prédictions IA
- Planifier les cultures et interventions
    ''',
    'data': [
        'security/ir.model.access.csv',
        'data/visibility.xml',
        'views/actions.xml',
        'views/main_menu.xml',
        'views/soil_type_views.xml',
        'views/exploitation_views.xml',
        'views/parcelle_views.xml',
        'views/culture_views.xml',
        'views/meteo_views.xml',
        'views/ia_predictions_views.xml',
        'views/intervention_views.xml',
        'views/intrants_views.xml',
        'views/utilisation_intrants_views.xml',
        'views/meteostat_import_views.xml',
        'views/alerte_climatique_views.xml',
        'views/tendance_climatique_views.xml',
        'data/security_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
    'license': 'LGPL-3',
}
