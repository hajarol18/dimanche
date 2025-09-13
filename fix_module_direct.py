#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour corriger le module directement
"""

import subprocess
import time

print("🔧 CORRECTION DIRECTE DU MODULE")
print("=" * 50)

def run_sql_command(sql):
    """Exécute une commande SQL via Docker"""
    try:
        command = f'docker exec -it odoo-18-docker-compose-master-db-1 psql -U odoo -d odoo123 -c "{sql}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

# 1. Supprimer complètement le module de la base de données
print("\n🗑️ Suppression du module de la base de données...")

sql_commands = [
    # Supprimer le module
    "DELETE FROM ir_module_module WHERE name = 'smart_agri_decision';",
    
    # Supprimer toutes les données liées
    "DELETE FROM ir_model_data WHERE module = 'smart_agri_decision';",
    
    # Supprimer les vues
    "DELETE FROM ir_ui_view WHERE model LIKE '%smart_agri%';",
    
    # Supprimer les menus
    "DELETE FROM ir_ui_menu WHERE name LIKE '%SmartAgri%';",
    
    # Supprimer les actions
    "DELETE FROM ir_actions_act_window WHERE res_model LIKE '%smart_agri%';",
    
    # Supprimer les champs
    "DELETE FROM ir_model_fields WHERE model LIKE '%smart_agri%';",
    
    # Supprimer les modèles
    "DELETE FROM ir_model WHERE model LIKE '%smart_agri%';",
    
    # Supprimer les tables
    "DROP TABLE IF EXISTS smart_agri_exploitation CASCADE;",
    "DROP TABLE IF EXISTS smart_agri_parcelle CASCADE;",
    "DROP TABLE IF EXISTS smart_agri_culture CASCADE;",
    "DROP TABLE IF EXISTS smart_agri_meteo CASCADE;",
    "DROP TABLE IF EXISTS smart_agri_alerte_climatique CASCADE;",
    "DROP TABLE IF EXISTS smart_agri_ai_model CASCADE;",
    "DROP TABLE IF EXISTS smart_agri_ia_predictions CASCADE;",
    "DROP TABLE IF EXISTS smart_agri_meteostat_import CASCADE;",
    "DROP TABLE IF EXISTS smart_agri_tendance_climatique CASCADE;",
    "DROP TABLE IF EXISTS smart_agri_scenario_climatique CASCADE;",
]

for i, sql in enumerate(sql_commands, 1):
    print(f"\n🔧 Exécution de la commande {i}/{len(sql_commands)}...")
    success, stdout, stderr = run_sql_command(sql)
    
    if success:
        print(f"✅ Succès")
        if stdout:
            print(f"   Output: {stdout.strip()}")
    else:
        print(f"❌ Erreur: {stderr.strip()}")

# 2. Redémarrer Odoo
print("\n🔄 Redémarrage d'Odoo...")
subprocess.run("docker-compose restart", shell=True)

# 3. Attendre
print("\n⏳ Attente du redémarrage...")
time.sleep(30)

# 4. Tester
print("\n🔍 Test de connexion...")
subprocess.run("python test_simple_connection.py", shell=True)

print("\n" + "=" * 50)
print("🎯 CORRECTION TERMINÉE")
print("🌐 Allez sur http://localhost:10020 pour tester")
