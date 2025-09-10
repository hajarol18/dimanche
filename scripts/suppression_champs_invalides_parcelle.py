#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de suppression des champs invalides dans demo_data_maroc.xml pour les parcelles
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
    
    # Champs à supprimer (avec leurs valeurs)
    champs_a_supprimer = [
        r'            <field name="pente">[^<]+</field>\n',
        r'            <field name="exposition">[^<]+</field>\n'
    ]
    
    # Appliquer les suppressions
    contenu_corrige = contenu
    for pattern in champs_a_supprimer:
        nb_suppressions = len(re.findall(pattern, contenu_corrige))
        if nb_suppressions > 0:
            contenu_corrige = re.sub(pattern, '', contenu_corrige)
            nom_champ = pattern.split('"')[1]
            print(f"✅ {nb_suppressions} occurrence(s) du champ '{nom_champ}' supprimée(s)")
    
    # Écrire le fichier corrigé
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(contenu_corrige)
    
    print(f"✅ Fichier {fichier} corrigé avec succès")
    
    return True

if __name__ == "__main__":
    print("🔧 SUPPRESSION DES CHAMPS INVALIDES DES PARCELLES DANS DEMO_DATA_MAROC.XML")
    print("=" * 80)
    
    success = corriger_fichier_xml()
    
    if success:
        print("\n✅ Script terminé avec succès")
        print("🎯 Maintenant vous pouvez essayer la mise à jour du module")
        print("📋 Champs supprimés :")
        print("   - pente (n'existe pas dans le modèle)")
        print("   - exposition (n'existe pas dans le modèle)")
    else:
        print("\n❌ Script terminé avec des erreurs")
