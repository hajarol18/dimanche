# -*- coding: utf-8 -*-

def migrate(cr, version):
    """Migration pour ajouter les champs manquants"""
    
    # Ajouter la colonne type_culture dans smart_agri_culture
    cr.execute("""
        ALTER TABLE smart_agri_culture 
        ADD COLUMN IF NOT EXISTS type_culture VARCHAR;
    """)
    
    # Ajouter la colonne date_prevue dans smart_agri_intervention
    cr.execute("""
        ALTER TABLE smart_agri_intervention 
        ADD COLUMN IF NOT EXISTS date_prevue DATE;
    """)
    
    # Ajouter la colonne statut_import dans smart_agri_meteostat_import
    cr.execute("""
        ALTER TABLE smart_agri_meteostat_import 
        ADD COLUMN IF NOT EXISTS statut_import VARCHAR;
    """)
    
    # Ajouter la colonne severite dans smart_agri_alerte_climatique
    cr.execute("""
        ALTER TABLE smart_agri_alerte_climatique 
        ADD COLUMN IF NOT EXISTS severite VARCHAR;
    """)
    
    # Ajouter la colonne statut dans smart_agri_ai_model
    cr.execute("""
        ALTER TABLE smart_agri_ai_model 
        ADD COLUMN IF NOT EXISTS statut VARCHAR;
    """)
    
    # Ajouter la colonne valeur_predite dans smart_agri_ia_predictions
    cr.execute("""
        ALTER TABLE smart_agri_ia_predictions 
        ADD COLUMN IF NOT EXISTS valeur_predite FLOAT;
    """)
    
    print("✅ Migration terminée - Tous les champs manquants ont été ajoutés")
