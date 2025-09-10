#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction de la valeur 'arboriculture' en 'fruits' pour le champ famille des cultures
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
    
    # Corrections des valeurs du champ famille
    # Le modèle utilise: cereales, legumineuses, oleagineux, fruits, legumes, autres
    corrections_valeurs = [
        ('arboriculture', 'fruits'),  # arboriculture -> fruits (valeur correcte)
    ]
    
    for ancienne_valeur, nouvelle_valeur in corrections_valeurs:
        nb_remplacements = contenu.count(f'>{ancienne_valeur}<')
        if nb_remplacements > 0:
            contenu = contenu.replace(f'>{ancienne_valeur}<', f'>{nouvelle_valeur}<')
            print(f"✅ {nb_remplacements} occurrence(s) de la valeur '{ancienne_valeur}' remplacée(s) par '{nouvelle_valeur}'")
    
    # Écrire le fichier corrigé
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(contenu)
    
    print(f"✅ Fichier {fichier} corrigé avec succès")
    
    return True

if __name__ == "__main__":
    print("🔧 CORRECTION DE LA VALEUR 'ARBORICULTURE' EN 'FRUITS'")
    print("=" * 70)
    
    success = corriger_fichier_xml()
    
    if success:
        print("\n✅ Script terminé avec succès")
        print("🎯 Maintenant vous pouvez essayer la mise à jour du module")
        print("📋 Correction appliquée :")
        print("   - arboriculture -> fruits (valeur correcte pour le champ famille)")
    else:
        print("\n❌ Script terminé avec des erreurs")
