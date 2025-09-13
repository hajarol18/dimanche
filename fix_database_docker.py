#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour corriger la base de données via Docker
"""

import subprocess
import sys

print("🔧 CORRECTION DE LA BASE DE DONNÉES VIA DOCKER")
print("=" * 50)

def run_docker_command(command):
    """Exécute une commande Docker"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command}")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ {command}")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

# 1. Vérifier l'état des conteneurs
print("\n📋 Vérification des conteneurs...")
run_docker_command("docker ps")

# 2. Se connecter à la base de données et corriger
print("\n🔧 Correction de la base de données...")

# Commandes SQL pour corriger le problème
sql_commands = [
    # Supprimer les données corrompues
    "DELETE FROM ir_model_data WHERE model LIKE '%smart_agri%' AND res_id = 0;",
    
    # Supprimer les vues corrompues
    "DELETE FROM ir_ui_view WHERE model LIKE '%smart_agri%' AND type = 'qweb';",
    
    # Supprimer les menus corrompus
    "DELETE FROM ir_ui_menu WHERE name LIKE '%SmartAgri%';",
    
    # Supprimer les actions corrompues
    "DELETE FROM ir_actions_act_window WHERE res_model LIKE '%smart_agri%';",
    
    # Nettoyer les données orphelines
    "DELETE FROM ir_model_data WHERE model LIKE '%smart_agri%' AND res_id NOT IN (SELECT id FROM smart_agri_exploitation UNION SELECT id FROM smart_agri_parcelle UNION SELECT id FROM smart_agri_culture UNION SELECT id FROM smart_agri_meteo UNION SELECT id FROM smart_agri_alerte_climatique UNION SELECT id FROM smart_agri_ai_model UNION SELECT id FROM smart_agri_ia_predictions UNION SELECT id FROM smart_agri_meteostat_import UNION SELECT id FROM smart_agri_tendance_climatique UNION SELECT id FROM smart_agri_scenario_climatique);",
    
    # Vider le cache
    "DELETE FROM ir_ui_view WHERE model LIKE '%smart_agri%' AND type = 'search';",
    "DELETE FROM ir_ui_view WHERE model LIKE '%smart_agri%' AND type = 'list';",
    "DELETE FROM ir_ui_view WHERE model LIKE '%smart_agri%' AND type = 'form';",
]

for i, sql in enumerate(sql_commands, 1):
    print(f"\n🔧 Exécution de la commande {i}/{len(sql_commands)}...")
    command = f'docker exec -it odoo-18-docker-compose-master-db-1 psql -U odoo -d odoo123 -c "{sql}"'
    run_docker_command(command)

# 3. Redémarrer Odoo
print("\n🔄 Redémarrage d'Odoo...")
run_docker_command("docker-compose restart")

print("\n" + "=" * 50)
print("🎯 CORRECTION TERMINÉE")
print("🌐 Allez sur http://localhost:10020 pour tester")
