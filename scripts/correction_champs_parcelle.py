#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction des champs dans demo_data_maroc.xml pour les parcelles
"""

import os

def corriger_fichier_xml():
    fichier = "addons/smart_agri_decision/data/demo_data_maroc.xml"
    
    if not os.path.exists(fichier):
        print(f"❌ Fichier {fichier} non trouvé")
        return False
    
    print(f"📝 Lecture du fichier {fichier}...")
    
    # Lire le fichier
    with open(fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Corrections à appliquer
    corrections = [
        ('soil_type_id', 'type_sol_id'),  # soil_type_id -> type_sol_id
        ('statut', 'state'),              # statut -> state (au cas où)
    ]
    
    # Appliquer les corrections
    contenu_corrige = contenu
    for champ_incorrect, champ_correct in corrections:
        nb_remplacements = contenu_corrige.count(f'name="{champ_incorrect}"')
        if nb_remplacements > 0:
            contenu_corrige = contenu_corrige.replace(
                f'name="{champ_incorrect}"',
                f'name="{champ_correct}"'
            )
            print(f"✅ {nb_remplacements} occurrence(s) de '{champ_incorrect}' remplacée(s) par '{champ_correct}'")
    
    # Écrire le fichier corrigé
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(contenu_corrige)
    
    print(f"✅ Fichier {fichier} corrigé avec succès")
    
    return True

if __name__ == "__main__":
    print("🔧 CORRECTION DES CHAMPS DES PARCELLES DANS DEMO_DATA_MAROC.XML")
    print("=" * 70)
    
    success = corriger_fichier_xml()
    
    if success:
        print("\n✅ Script terminé avec succès")
        print("🎯 Maintenant vous pouvez essayer la mise à jour du module")
        print("📋 Champs corrigés :")
        print("   - soil_type_id -> type_sol_id")
        print("   - statut -> state (si nécessaire)")
    else:
        print("\n❌ Script terminé avec des erreurs")
