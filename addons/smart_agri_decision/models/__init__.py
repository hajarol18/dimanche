# -*- coding: utf-8 -*-

# 1. MODÈLES DE BASE (sans dépendances)
from . import smart_agri_soil_type

# 2. MODÈLES AVEC DÉPENDANCES SIMPLES
from . import smart_agri_exploitation

# 3. MODÈLES AVEC DÉPENDANCES COMPLEXES
from . import smart_agri_parcelle
from . import smart_agri_parcelle_map
from . import smart_agri_culture
from . import smart_agri_meteo
from . import smart_agri_intervention
from . import smart_agri_intrants
from . import smart_agri_utilisation_intrant
from . import smart_agri_geojson_wizard

# 4. MODÈLES SPÉCIALISÉS
from . import smart_agri_ia_predictions
from . import smart_agri_rotation_culturelle
from . import smart_agri_objectif_rotation
from . import smart_agri_rcp_scenario
from . import smart_agri_scenario_climatique
from . import smart_agri_dashboard
from . import smart_agri_tableau_bord

# 5. MODÈLES CLIMATIQUES
from . import smart_agri_station_meteo
from . import smart_agri_meteostat_import
from . import smart_agri_alerte_climatique
from . import smart_agri_tendance_climatique
# TEMPORAIREMENT COMMENTÉ POUR RÉSOLUDRE L'ERREUR DE CHARGEMENT
# from . import smart_agri_alerte_exploitation

# 6. MODÈLES IA
from . import ia_dashboard
from . import ia_simulateur
from . import ia_detection_stress
from . import ia_optimisation_ressources
# ÉTAPE 1 : RÉACTIVATION DU MODÈLE IA DE BASE
from . import smart_agri_ai_model
# from . import smart_agri_ai_prediction

# 7. MODÈLES CLIMATIQUES AVANCÉS
# TEMPORAIREMENT COMMENTÉ POUR RÉSOLUDRE L'ERREUR DE CHARGEMENT
# from . import smart_agri_climate_data
