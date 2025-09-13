#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour corriger l'erreur de clé dupliquée
"""

import subprocess
import time

print("🔧 CORRECTION DE L'ERREUR DE CLÉ DUPLIQUÉE")
print("=" * 50)

def run_sql_command(sql):
    """Exécute une commande SQL via Docker"""
    try:
        command = f'docker exec -it odoo-18-docker-compose-master-db-1 psql -U odoo -d odoo123 -c "{sql}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

# 1. Supprimer les données dupliquées
print("\n🗑️ Suppression des données dupliquées...")

sql_commands = [
    # Supprimer les données dupliquées dans ir_model_data
    "DELETE FROM ir_model_data WHERE module = 'base' AND name = 'module_smart_agri_decision';",
    
    # Supprimer les données orphelines
    "DELETE FROM ir_model_data WHERE module = 'smart_agri_decision' AND res_id = 0;",
    
    # Nettoyer les vues dupliquées
    "DELETE FROM ir_ui_view WHERE model = 'smart_agri_exploitation' AND id NOT IN (SELECT MIN(id) FROM ir_ui_view WHERE model = 'smart_agri_exploitation' GROUP BY name);",
    
    # Nettoyer les actions dupliquées
    "DELETE FROM ir_actions_act_window WHERE res_model = 'smart_agri_exploitation' AND id NOT IN (SELECT MIN(id) FROM ir_actions_act_window WHERE res_model = 'smart_agri_exploitation');",
    
    # Nettoyer les menus dupliqués
    "DELETE FROM ir_ui_menu WHERE name LIKE '%SmartAgri%' AND id NOT IN (SELECT MIN(id) FROM ir_ui_menu WHERE name LIKE '%SmartAgri%' GROUP BY name);",
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

print("\n" + "=" * 50)
print("🎯 CORRECTION TERMINÉE")
print("🌐 Allez sur http://localhost:10020 pour tester")
