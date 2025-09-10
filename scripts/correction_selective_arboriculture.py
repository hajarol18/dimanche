#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction sélective de 'arboriculture' en 'fruits' seulement dans le champ famille des cultures
"""

import os
import re

def corriger_fichier_xml():
    fichier = "addons/smart_agri_decision/data/demo_data_maroc.xml"
    
    if not os.path.exists(fichier):
        print(f"❌ Fichier {fichier} non trouvé")
        return False
    
    print(f"📝 Lecture du fichier {fichier}...")
    
    # Lire le fichier
    with open(fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Correction sélective : seulement dans le champ famille des cultures
    # Pattern pour trouver le champ famille dans les cultures
    pattern_culture_famille = r'(<field name="famille">)arboriculture(</field>)'
    
    # Remplacer seulement dans ce contexte
    contenu_corrige = re.sub(pattern_culture_famille, r'\1fruits\2', contenu)
    
    # Compter les remplacements
    nb_remplacements = contenu.count('arboriculture') - contenu_corrige.count('arboriculture')
    
    if nb_remplacements > 0:
        print(f"✅ {nb_remplacements} occurrence(s) de 'arboriculture' corrigée(s) en 'fruits' dans le champ famille des cultures")
    else:
        print("✅ Aucune correction nécessaire")
    
    # Écrire le fichier corrigé
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(contenu_corrige)
    
    print(f"✅ Fichier {fichier} corrigé avec succès")
    
    return True

if __name__ == "__main__":
    print("🔧 CORRECTION SÉLECTIVE D'ARBORICULTURE EN FRUITS (CULTURES SEULEMENT)")
    print("=" * 80)
    
    success = corriger_fichier_xml()
    
    if success:
        print("\n✅ Script terminé avec succès")
        print("🎯 Maintenant vous pouvez essayer la mise à jour du module")
        print("📋 Correction appliquée :")
        print("   - arboriculture -> fruits (seulement dans le champ famille des cultures)")
        print("   - type_exploitation des exploitations conservé (arboriculture est valide)")
    else:
        print("\n❌ Script terminé avec des erreurs")
