#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'ajout du champ surface_utilisee manquant aux cultures dans demo_data_maroc.xml
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
    
    # Chercher toutes les cultures et ajouter surface_utilisee
    pattern_culture = r'(<record id="[^"]+" model="smart_agri_culture">.*?<field name="famille">[^<]+</field>.*?)(</record>)'
    
    def ajouter_surface(match):
        culture_content = match.group(1)
        # Ajouter surface_utilisee après famille
        if 'surface_utilisee' not in culture_content:
            # Déterminer la surface basée sur le nom de la culture
            if 'ble' in culture_content.lower():
                surface = '45.0'  # Surface pour le blé
            elif 'orange' in culture_content.lower() or 'agrumes' in culture_content.lower():
                surface = '30.0'  # Surface pour les agrumes
            else:
                surface = '25.0'  # Surface par défaut
            
            # Insérer après le champ famille
            culture_content = culture_content.replace(
                '</field>',
                f'</field>\n            <field name="surface_utilisee">{surface}</field>',
                1
            )
        
        return culture_content + match.group(2)
    
    # Appliquer la correction
    contenu_corrige = re.sub(pattern_culture, ajouter_surface, contenu, flags=re.DOTALL)
    
    # Compter les ajouts
    nb_cultures_avant = len(re.findall(r'<record id="[^"]+" model="smart_agri_culture">', contenu))
    nb_cultures_apres = len(re.findall(r'<record id="[^"]+" model="smart_agri_culture">', contenu_corrige))
    nb_surfaces_ajoutees = contenu_corrige.count('surface_utilisee') - contenu.count('surface_utilisee')
    
    print(f"✅ {nb_surfaces_ajoutees} champ(s) surface_utilisee ajouté(s) aux cultures")
    
    # Écrire le fichier corrigé
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(contenu_corrige)
    
    print(f"✅ Fichier {fichier} corrigé avec succès")
    
    return True

if __name__ == "__main__":
    print("🔧 AJOUT DU CHAMP SURFACE_UTILISEE AUX CULTURES")
    print("=" * 60)
    
    success = corriger_fichier_xml()
    
    if success:
        print("\n✅ Script terminé avec succès")
        print("🎯 Maintenant vous pouvez essayer la mise à jour du module")
        print("📋 Correction appliquée :")
        print("   - surface_utilisee ajouté aux cultures (champ obligatoire)")
        print("   - Valeurs adaptées selon le type de culture")
    else:
        print("\n❌ Script terminé avec des erreurs")
