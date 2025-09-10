#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de vérification - Remplacement complet des données françaises par des données marocaines
"""

import os
import xml.etree.ElementTree as ET

def test_verification_maroc():
    """Teste que toutes les données françaises ont été remplacées par des données marocaines"""
    
    print("🇲🇦 VÉRIFICATION COMPLÈTE DES DONNÉES MAROCAINES...")
    print("=" * 60)
    
    # Fichiers à vérifier
    fichiers_a_verifier = [
        "data/donnees_supplementaires.xml",
        "data/donnees_maroc_finales.xml",
        "data/demo_data_maroc.xml",
        "data/donnees_maroc_completes.xml",
        "data/donnees_maroc_etendues.xml"
    ]
    
    # Mots-clés français à détecter
    mots_cles_francais = [
        "Provence", "Nouvelle-Aquitaine", "Hauts-de-France", "Auvergne", "Occitanie", "Bretagne",
        "Pierre Durand", "Sophie Moreau", "48.8580", "2.3580", "Paris", "Lyon", "Marseille",
        "Coopérative du Soleil", "Domaine des Coteaux", "EARL des Grands Champs", "GAEC des Trois Chênes"
    ]
    
    # Mots-clés marocains à vérifier
    mots_cles_marocains = [
        "Maroc", "Casablanca", "Rabat", "Agadir", "Meknès", "Mohammedia", "Doukkala", "Souss",
        "Ahmed Benali", "Fatima Alaoui", "Mohammed Alami", "Amina Tazi", "Coopérative Al Baraka",
        "33.9716", "-6.8498", "32.2540", "-8.5102", "30.4278", "-9.5981"
    ]
    
    total_fichiers_verifies = 0
    total_donnees_marocaines = 0
    total_donnees_francaises = 0
    
    print("🔍 ANALYSE DES FICHIERS DE DONNÉES...")
    print("-" * 40)
    
    for fichier in fichiers_a_verifier:
        if os.path.exists(fichier):
            print(f"✅ Fichier trouvé : {fichier}")
            total_fichiers_verifies += 1
            
            try:
                tree = ET.parse(fichier)
                root = tree.getroot()
                
                # Vérification des données françaises
                contenu_fichier = ET.tostring(root, encoding='unicode')
                donnees_francaises_trouvees = []
                
                for mot_cle in mots_cles_francais:
                    if mot_cle in contenu_fichier:
                        donnees_francaises_trouvees.append(mot_cle)
                        total_donnees_francaises += 1
                
                # Vérification des données marocaines
                donnees_marocaines_trouvees = []
                for mot_cle in mots_cles_marocains:
                    if mot_cle in contenu_fichier:
                        donnees_marocaines_trouvees.append(mot_cle)
                        total_donnees_marocaines += 1
                
                # Affichage des résultats
                if donnees_francaises_trouvees:
                    print(f"   ⚠️  DONNÉES FRANÇAISES DÉTECTÉES : {', '.join(donnees_francaises_trouvees)}")
                else:
                    print(f"   ✅ Aucune donnée française détectée")
                
                if donnees_marocaines_trouvees:
                    print(f"   🇲🇦 DONNÉES MAROCAINES DÉTECTÉES : {', '.join(donnees_marocaines_trouvees[:5])}...")
                else:
                    print(f"   ❌ Aucune donnée marocaine détectée")
                
                # Comptage des enregistrements
                exploitations = root.findall('.//record[@model="smart_agri_exploitation"]')
                parcelles = root.findall('.//record[@model="smart_agri_parcelle"]')
                cultures = root.findall('.//record[@model="smart_agri_culture"]')
                types_sol = root.findall('.//record[@model="smart_agri_soil_type"]')
                
                print(f"   📊 Contenu : {len(exploitations)} exploitations, {len(parcelles)} parcelles, {len(cultures)} cultures, {len(types_sol)} types de sol")
                
            except ET.ParseError as e:
                print(f"   ❌ Erreur XML : {e}")
                
        else:
            print(f"❌ Fichier manquant : {fichier}")
    
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 60)
    
    print(f"📁 Fichiers vérifiés : {total_fichiers_verifies}")
    print(f"🇲🇦 Données marocaines détectées : {total_donnees_marocaines}")
    print(f"🇫🇷 Données françaises détectées : {total_donnees_francaises}")
    
    if total_donnees_francaises == 0:
        print("\n🎉 SUCCÈS : Aucune donnée française détectée !")
        print("✅ Toutes les données sont maintenant marocaines")
    else:
        print(f"\n⚠️  ATTENTION : {total_donnees_francaises} données françaises encore présentes")
        print("🔧 Nécessite un nettoyage supplémentaire")
    
    # Vérification du manifest
    print(f"\n📋 VÉRIFICATION DU MANIFEST :")
    manifest = "__manifest__.py"
    if os.path.exists(manifest):
        with open(manifest, 'r', encoding='utf-8') as f:
            contenu = f.read()
            if 'donnees_maroc_finales.xml' in contenu:
                print("✅ Fichier de données marocaines finales référencé dans le manifest")
            else:
                print("❌ Fichier de données marocaines finales NON référencé dans le manifest")
    else:
        print("❌ Manifest manquant")
    
    print(f"\n🎯 RECOMMANDATIONS FINALES :")
    if total_donnees_francaises == 0:
        print("   ✅ Module prêt pour la production - 100% marocain")
        print("   ✅ Mettre à jour le module dans Odoo")
        print("   ✅ Vérifier l'affichage dans l'interface")
    else:
        print("   🔧 Nettoyer les données françaises restantes")
        print("   🔧 Vérifier les références dans les modèles")
        print("   🔧 Relancer la vérification après nettoyage")
    
    return total_donnees_francaises == 0

if __name__ == "__main__":
    test_verification_maroc()
