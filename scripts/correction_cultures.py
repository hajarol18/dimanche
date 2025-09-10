#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction des cultures dans demo_data_maroc.xml
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
    
    # Corrections à appliquer
    corrections = [
        # type_culture -> famille
        (r'<field name="type_culture">([^<]+)</field>', r'<field name="famille">\1</field>'),
        
        # date_semis -> date_plantation
        (r'<field name="date_semis"', r'<field name="date_plantation"'),
        
        # date_recolte -> date_recolte_reelle
        (r'<field name="date_recolte"', r'<field name="date_recolte_reelle"'),
        
        # rendement_attendu -> rendement_moyen
        (r'<field name="rendement_attendu">([^<]+)</field>', r'<field name="rendement_moyen">\1</field>'),
        
        # rendement_reel -> rendement_reel (garder)
        # state -> state (garder, mais vérifier les valeurs)
    ]
    
    # Appliquer les corrections
    contenu_corrige = contenu
    for pattern, replacement in corrections:
        nb_remplacements = len(re.findall(pattern, contenu_corrige))
        if nb_remplacements > 0:
            contenu_corrige = re.sub(pattern, replacement, contenu_corrige)
            nom_champ_ancien = pattern.split('"')[1]
            nom_champ_nouveau = replacement.split('"')[1]
            print(f"✅ {nb_remplacements} occurrence(s) de '{nom_champ_ancien}' remplacée(s) par '{nom_champ_nouveau}'")
    
    # Corriger les valeurs de state pour les cultures
    # Le modèle utilise: planifiee, active, recoltee, abandonnee
    corrections_valeurs = [
        ('termine', 'recoltee'),  # termine -> recoltee
    ]
    
    for ancienne_valeur, nouvelle_valeur in corrections_valeurs:
        nb_remplacements = contenu_corrige.count(f'>{ancienne_valeur}<')
        if nb_remplacements > 0:
            contenu_corrige = contenu_corrige.replace(f'>{ancienne_valeur}<', f'>{nouvelle_valeur}<')
            print(f"✅ {nb_remplacements} occurrence(s) de la valeur '{ancienne_valeur}' remplacée(s) par '{nouvelle_valeur}'")
    
    # Écrire le fichier corrigé
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(contenu_corrige)
    
    print(f"✅ Fichier {fichier} corrigé avec succès")
    
    return True

if __name__ == "__main__":
    print("🔧 CORRECTION DES CULTURES DANS DEMO_DATA_MAROC.XML")
    print("=" * 60)
    
    success = corriger_fichier_xml()
    
    if success:
        print("\n✅ Script terminé avec succès")
        print("🎯 Maintenant vous pouvez essayer la mise à jour du module")
        print("📋 Corrections appliquées :")
        print("   - type_culture -> famille")
        print("   - date_semis -> date_plantation")
        print("   - date_recolte -> date_recolte_reelle")
        print("   - rendement_attendu -> rendement_moyen")
        print("   - termine -> recoltee (pour state)")
    else:
        print("\n❌ Script terminé avec des erreurs")
