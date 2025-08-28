#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de nettoyage du cache Odoo pour SmartAgriDecision
"""

import os
import sys
import shutil

def clean_odoo_cache():
    """Nettoie le cache d'Odoo et force le rechargement"""
    
    print("🧹 Nettoyage du cache Odoo...")
    
    # Chemins de cache potentiels
    cache_paths = [
        "~/.cache/odoo",
        "~/.local/share/odoo",
        "/tmp/odoo_cache",
        "C:/Users/Hajar/AppData/Local/Temp/odoo",
        "C:/Users/Hajar/AppData/Roaming/odoo"
    ]
    
    for path in cache_paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            try:
                shutil.rmtree(expanded_path)
                print(f"✅ Cache supprimé: {expanded_path}")
            except Exception as e:
                print(f"⚠️ Erreur lors de la suppression de {expanded_path}: {e}")
    
    print("✅ Nettoyage terminé!")
    print("\n📋 Instructions:")
    print("1. Redémarre Odoo complètement")
    print("2. Va dans Apps > Recherche 'SmartAgriDecision'")
    print("3. Désinstalle le module s'il est installé")
    print("4. Réinstalle le module")
    print("5. Les données seront chargées automatiquement")

if __name__ == "__main__":
    clean_odoo_cache()
