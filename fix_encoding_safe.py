#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour corriger l'encodage sans supprimer le travail
"""

import os
import shutil

print("🔧 CORRECTION DE L'ENCODAGE SANS SUPPRIMER LE TRAVAIL")
print("=" * 60)

def fix_file_encoding(file_path):
    """Corrige l'encodage d'un fichier"""
    try:
        # Lire le fichier en mode binaire
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Décoder en UTF-8 en ignorant les erreurs
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            text = content.decode('utf-8', errors='ignore')
        
        # Supprimer les caractères null
        text = text.replace('\x00', '')
        
        # Réécrire le fichier proprement
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✅ Corrigé: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur {file_path}: {e}")
        return False

# Fichiers à corriger
files_to_fix = [
    "addons/smart_agri_decision/__init__.py",
    "addons/smart_agri_decision/models/__init__.py",
    "addons/smart_agri_decision/models/smart_agri_exploitation.py",
    "addons/smart_agri_decision/__manifest__.py",
    "addons/smart_agri_decision/views/exploitation_views.xml"
]

print("\n🔧 Correction des fichiers...")

for file_path in files_to_fix:
    if os.path.exists(file_path):
        fix_file_encoding(file_path)
    else:
        print(f"⚠️ Fichier non trouvé: {file_path}")

print("\n" + "=" * 60)
print("🎯 CORRECTION TERMINÉE")
print("🌐 Redémarrez Odoo et essayez d'installer le module")
