#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour réinitialiser complètement le module
"""

import subprocess
import sys

print("🔄 RÉINITIALISATION COMPLÈTE DU MODULE")
print("=" * 50)

def run_command(command):
    """Exécute une commande"""
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

# 1. Arrêter les conteneurs
print("\n🛑 Arrêt des conteneurs...")
run_command("docker-compose down")

# 2. Supprimer complètement la base de données
print("\n🗑️ Suppression de la base de données...")
run_command("docker volume rm odoo-18-docker-compose-master_db_data")

# 3. Supprimer le module du système de fichiers
print("\n🗑️ Suppression du module...")
run_command("rm -rf addons/smart_agri_decision")

# 4. Recréer le module de base
print("\n🔧 Recréation du module de base...")
run_command("mkdir -p addons/smart_agri_decision")

# 5. Créer un manifest minimal
manifest_content = '''{
    "name": "SmartAgriDecision",
    "version": "18.0.1.0.0",
    "category": "Agriculture",
    "summary": "Module d'aide à la décision agricole basé sur l'IA",
    "description": "Module Odoo 18 pour l'aide à la décision en agriculture",
    "author": "Hajar",
    "website": "https://www.odoo.com",
    "depends": ["base", "mail"],
    "data": [],
    "installable": True,
    "auto_install": False,
    "application": True,
}'''

with open("addons/smart_agri_decision/__manifest__.py", "w") as f:
    f.write(manifest_content)

# 6. Créer un __init__.py minimal
with open("addons/smart_agri_decision/__init__.py", "w") as f:
    f.write("# -*- coding: utf-8 -*-\n")

# 7. Créer un models/__init__.py minimal
run_command("mkdir -p addons/smart_agri_decision/models")
with open("addons/smart_agri_decision/models/__init__.py", "w") as f:
    f.write("# -*- coding: utf-8 -*-\n")

# 8. Redémarrer les conteneurs
print("\n🚀 Redémarrage des conteneurs...")
run_command("docker-compose up -d")

# 9. Attendre que Odoo démarre
print("\n⏳ Attente du démarrage d'Odoo...")
import time
time.sleep(30)

# 10. Tester la connexion
print("\n🔍 Test de connexion...")
run_command("python test_simple_connection.py")

print("\n" + "=" * 50)
print("🎯 RÉINITIALISATION TERMINÉE")
print("🌐 Allez sur http://localhost:10020 pour tester")
