#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction finale des cultures dans demo_data_maroc.xml
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
    
    # Champs à supprimer (n'existent pas dans le modèle)
    champs_a_supprimer = [
        r'            <field name="variete">[^<]+</field>\n',
    ]
    
    # Appliquer les suppressions
    contenu_corrige = contenu
    for pattern in champs_a_supprimer:
        nb_suppressions = len(re.findall(pattern, contenu_corrige))
        if nb_suppressions > 0:
            contenu_corrige = re.sub(pattern, '', contenu_corrige)
            nom_champ = pattern.split('"')[1]
            print(f"✅ {nb_suppressions} occurrence(s) du champ '{nom_champ}' supprimée(s)")
    
    # Vérifier s'il y a d'autres champs potentiellement problématiques
    # Chercher tous les champs dans les cultures
    pattern_cultures = r'<record id="[^"]+" model="smart_agri_culture">(.*?)</record>'
    cultures = re.findall(pattern_cultures, contenu_corrige, re.DOTALL)
    
    print(f"\n🔍 Vérification des champs dans {len(cultures)} culture(s)...")
    
    # Champs valides selon le modèle
    champs_valides = {
        'name', 'code', 'exploitation_id', 'parcelle_id', 'description',
        'famille', 'duree_cycle', 'saison_plantation', 'rendement_moyen',
        'surface_utilisee', 'date_plantation', 'date_recolte_prevue',
        'date_recolte_reelle', 'state', 'rendement_reel', 'qualite_recolte',
        'observations', 'problemes_rencontres', 'solutions_appliquees',
        'active', 'notes'
    }
    
    for i, culture in enumerate(cultures):
        # Extraire tous les noms de champs
        champs_trouves = re.findall(r'<field name="([^"]+)">', culture)
        champs_invalides = [champ for champ in champs_trouves if champ not in champs_valides]
        
        if champs_invalides:
            print(f"⚠️  Culture {i+1} : champs invalides détectés : {champs_invalides}")
    
    # Écrire le fichier corrigé
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(contenu_corrige)
    
    print(f"✅ Fichier {fichier} corrigé avec succès")
    
    return True

if __name__ == "__main__":
    print("🔧 CORRECTION FINALE DES CULTURES DANS DEMO_DATA_MAROC.XML")
    print("=" * 70)
    
    success = corriger_fichier_xml()
    
    if success:
        print("\n✅ Script terminé avec succès")
        print("🎯 Maintenant vous pouvez essayer la mise à jour du module")
        print("📋 Correction appliquée :")
        print("   - variete supprimé (champ inexistant)")
        print("   - Vérification des autres champs effectuée")
    else:
        print("\n❌ Script terminé avec des erreurs")
