#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour corriger directement la base de données
"""

import psycopg2
import sys

print("🔧 CORRECTION DIRECTE DE LA BASE DE DONNÉES")
print("=" * 50)

try:
    # Connexion directe à PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="odoo123",
        user="odoo",
        password="odoo"
    )
    
    cur = conn.cursor()
    print("✅ Connexion à la base de données réussie")
    
    # 1. Chercher des données corrompues dans ir_model_data
    print("\n🔍 Recherche de données corrompues...")
    
    # Chercher des enregistrements avec des problèmes de champs
    cur.execute("""
        SELECT id, name, model, res_id 
        FROM ir_model_data 
        WHERE model LIKE '%smart_agri%' 
        ORDER BY id DESC 
        LIMIT 10
    """)
    
    results = cur.fetchall()
    print(f"✅ Enregistrements trouvés: {len(results)}")
    
    for row in results:
        print(f"   - ID: {row[0]}, Name: {row[1]}, Model: {row[2]}, Res ID: {row[3]}")
    
    # 2. Vérifier les tables des modèles
    print("\n📊 Vérification des tables...")
    
    tables_to_check = [
        'smart_agri_exploitation',
        'smart_agri_parcelle', 
        'smart_agri_culture',
        'smart_agri_meteo',
        'smart_agri_alerte_climatique',
        'smart_agri_ai_model',
        'smart_agri_ia_predictions',
        'smart_agri_meteostat_import',
        'smart_agri_tendance_climatique',
        'smart_agri_scenario_climatique'
    ]
    
    for table in tables_to_check:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"✅ {table}: {count} enregistrements")
        except Exception as e:
            print(f"❌ {table}: Erreur - {str(e)[:50]}...")
    
    # 3. Nettoyer les données corrompues
    print("\n🧹 Nettoyage des données corrompues...")
    
    # Supprimer les données orphelines
    cur.execute("""
        DELETE FROM ir_model_data 
        WHERE model LIKE '%smart_agri%' 
        AND res_id NOT IN (
            SELECT id FROM smart_agri_exploitation
            UNION
            SELECT id FROM smart_agri_parcelle
            UNION
            SELECT id FROM smart_agri_culture
            UNION
            SELECT id FROM smart_agri_meteo
            UNION
            SELECT id FROM smart_agri_alerte_climatique
            UNION
            SELECT id FROM smart_agri_ai_model
            UNION
            SELECT id FROM smart_agri_ia_predictions
            UNION
            SELECT id FROM smart_agri_meteostat_import
            UNION
            SELECT id FROM smart_agri_tendance_climatique
            UNION
            SELECT id FROM smart_agri_scenario_climatique
        )
    """)
    
    deleted = cur.rowcount
    print(f"✅ {deleted} enregistrements orphelins supprimés")
    
    # 4. Vider le cache
    print("\n🗑️ Vidage du cache...")
    
    cur.execute("DELETE FROM ir_ui_view WHERE model LIKE '%smart_agri%' AND type = 'qweb'")
    print(f"✅ {cur.rowcount} vues QWeb supprimées")
    
    cur.execute("DELETE FROM ir_ui_menu WHERE name LIKE '%SmartAgri%'")
    print(f"✅ {cur.rowcount} menus supprimés")
    
    # Valider les changements
    conn.commit()
    print("✅ Changements validés")
    
    cur.close()
    conn.close()
    
    print("\n" + "=" * 50)
    print("🎯 CORRECTION TERMINÉE")
    print("🔄 Redémarrez Odoo pour appliquer les changements")
    
except psycopg2.Error as e:
    print(f"❌ Erreur base de données: {e}")
except Exception as e:
    print(f"❌ Erreur générale: {e}")

print("\n🌐 Allez sur http://localhost:10020 après redémarrage")
