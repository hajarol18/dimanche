# -*- coding: utf-8 -*-

# Import des modèles de base
from . import smart_agri_exploitation
from . import smart_agri_soil_type
from . import smart_agri_parcelle
from . import smart_agri_culture
from . import smart_agri_intervention
from . import smart_agri_intrants
from . import smart_agri_utilisation_intrant

# Import des modèles météo et climat
from . import smart_agri_meteo
from . import smart_agri_meteostat_import
from . import smart_agri_tendance_climatique
from . import smart_agri_alerte_climatique
from . import smart_agri_alerte_exploitation
from . import smart_agri_rcp_scenario
from . import smart_agri_scenario_climatique

# Import des modèles IA
from . import smart_agri_ia_predictions
from . import ia_detection_stress
from . import ia_optimisation_ressources
from . import ia_dashboard
from . import smart_agri_ai_model
from . import ia_simulateur

# Import des modèles d'analyse
from . import smart_agri_tableau_bord
from . import smart_agri_dashboard
from . import smart_agri_rotation_culturelle
from . import smart_agri_objectif_rotation
