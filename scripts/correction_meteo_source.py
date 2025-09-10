#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction du champ source_donnees en source dans les données météo
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
    
    # Correction : source_donnees -> source pour les données météo
    # Pattern pour trouver le champ source_donnees
    pattern_source = r'<field name="source_donnees">([^<]+)</field>'
    
    # Remplacer par le champ source avec une valeur appropriée
    def remplacer_source(match):
        ancienne_valeur = match.group(1)
        # Mapper les anciennes valeurs vers les nouvelles valeurs du modèle
        if 'Direction Météorologie Nationale Maroc' in ancienne_valeur:
            return '<field name="source">station_locale</field>'
        elif 'Meteostat' in ancienne_valeur:
            return '<field name="source">meteostat</field>'
        else:
            return '<field name="source">autre</field>'
    
    contenu_corrige = re.sub(pattern_source, remplacer_source, contenu)
    
    # Compter les remplacements
    nb_remplacements = contenu.count('source_donnees') - contenu_corrige.count('source_donnees')
    
    if nb_remplacements > 0:
        print(f"✅ {nb_remplacements} occurrence(s) de 'source_donnees' corrigée(s) en 'source'")
    else:
        print("✅ Aucune correction nécessaire")
    
    # Écrire le fichier corrigé
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(contenu_corrige)
    
    print(f"✅ Fichier {fichier} corrigé avec succès")
    
    return True

if __name__ == "__main__":
    print("🔧 CORRECTION DU CHAMP SOURCE_DONNEES EN SOURCE DANS LES DONNÉES MÉTÉO")
    print("=" * 80)
    
    success = corriger_fichier_xml()
    
    if success:
        print("\n✅ Script terminé avec succès")
        print("🎯 Maintenant vous pouvez essayer la mise à jour du module")
        print("📋 Correction appliquée :")
        print("   - source_donnees -> source (champ correct pour les données météo)")
        print("   - Valeurs mappées vers les sélections valides du modèle")
    else:
        print("\n❌ Script terminé avec des erreurs")
