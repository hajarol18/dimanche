#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction finale des parcelles dans demo_data_maroc.xml
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
    
    # Remplacer state par active pour les parcelles
    nb_remplacements = contenu.count('name="state">active')
    if nb_remplacements > 0:
        contenu = contenu.replace('name="state">active', 'name="active">True')
        print(f"✅ {nb_remplacements} occurrence(s) de 'state'>active remplacée(s) par 'active'>True")
    
    # Écrire le fichier corrigé
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(contenu)
    
    print(f"✅ Fichier {fichier} corrigé avec succès")
    
    return True

if __name__ == "__main__":
    print("🔧 CORRECTION FINALE DES PARCELLES DANS DEMO_DATA_MAROC.XML")
    print("=" * 70)
    
    success = corriger_fichier_xml()
    
    if success:
        print("\n✅ Script terminé avec succès")
        print("🎯 Maintenant vous pouvez essayer la mise à jour du module")
        print("📋 Correction appliquée :")
        print("   - state -> active (champ correct pour les parcelles)")
    else:
        print("\n❌ Script terminé avec des erreurs")
