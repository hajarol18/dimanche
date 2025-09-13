#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour corriger le problème Float ondelete
"""

import os
import re

print("🔧 CORRECTION DU PROBLÈME FLOAT ONDELETE")
print("=" * 50)

# Dossier des modèles
models_dir = "addons/smart_agri_decision/models"

# Chercher tous les fichiers Python
python_files = []
for root, dirs, files in os.walk(models_dir):
    for file in files:
        if file.endswith('.py'):
            python_files.append(os.path.join(root, file))

print(f"📁 Fichiers Python trouvés: {len(python_files)}")

# Chercher des problèmes potentiels
issues_found = 0

for file_path in python_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher des patterns problématiques
        patterns_to_check = [
            r'fields\.Float\([^)]*ondelete[^)]*\)',
            r'Float\([^)]*ondelete[^)]*\)',
            r'ondelete[^)]*Float\([^)]*\)',
        ]
        
        for pattern in patterns_to_check:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"❌ Problème trouvé dans {file_path}:")
                for match in matches:
                    print(f"   - {match}")
                issues_found += 1
        
        # Chercher des champs Float avec des attributs incorrects
        float_pattern = r'(\w+)\s*=\s*fields\.Float\([^)]*\)'
        float_matches = re.findall(float_pattern, content)
        
        for field_name in float_matches:
            # Vérifier si ce champ a des attributs incorrects
            field_def_pattern = rf'{field_name}\s*=\s*fields\.Float\([^)]*ondelete[^)]*\)'
            if re.search(field_def_pattern, content):
                print(f"❌ Champ Float avec ondelete incorrect dans {file_path}: {field_name}")
                issues_found += 1
    
    except Exception as e:
        print(f"❌ Erreur lecture {file_path}: {e}")

if issues_found == 0:
    print("✅ Aucun problème Float ondelete trouvé dans le code")
else:
    print(f"❌ {issues_found} problèmes trouvés")

# Vérifier les fichiers de données XML
print("\n🔍 Vérification des fichiers XML...")
data_dir = "addons/smart_agri_decision/data"
xml_files = []

for root, dirs, files in os.walk(data_dir):
    for file in files:
        if file.endswith('.xml'):
            xml_files.append(os.path.join(root, file))

print(f"📁 Fichiers XML trouvés: {len(xml_files)}")

xml_issues = 0
for file_path in xml_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher des patterns problématiques dans XML
        if 'ondelete' in content and 'Float' in content:
            print(f"❌ Fichier XML suspect: {file_path}")
            xml_issues += 1
    
    except Exception as e:
        print(f"❌ Erreur lecture {file_path}: {e}")

if xml_issues == 0:
    print("✅ Aucun problème trouvé dans les fichiers XML")
else:
    print(f"❌ {xml_issues} fichiers XML suspects")

print("\n" + "=" * 50)
print("🎯 VÉRIFICATION TERMINÉE")

if issues_found == 0 and xml_issues == 0:
    print("✅ Aucun problème trouvé dans le code")
    print("🔍 Le problème pourrait venir d'un cache ou d'une migration")
    print("💡 Solution: Redémarrez Odoo complètement")
else:
    print("❌ Des problèmes ont été trouvés dans le code")
    print("💡 Solution: Corrigez les fichiers identifiés")
