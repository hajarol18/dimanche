#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification finale - Vérification de l'absence de données françaises après nettoyage intelligent
"""

import os
import re
import glob

def verification_finale_maroc():
    """Vérifie l'absence de données françaises après le nettoyage intelligent final"""
    
    print("🔍 VÉRIFICATION FINALE - ABSENCE DE DONNÉES FRANÇAISES")
    print("=" * 80)
    
    # Mots-clés français à détecter (vraies références françaises)
    mots_francais = [
        'France', 'Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Toulouse', 'Nantes',
        'Strasbourg', 'Montpellier', 'Lille', 'Rennes', 'Reims', 'Saint-Étienne',
        'Toulon', 'Angers', 'Grenoble', 'Dijon', 'Nîmes', 'Saint-Denis',
        'Provence', 'Aquitaine', 'Bretagne', 'Bourgogne', 'Centre', 'Champagne',
        'Franche-Comté', 'Île-de-France', 'Languedoc', 'Limousin', 'Lorraine',
        'Midi-Pyrénées', 'Nord-Pas-de-Calais', 'Normandie', 'Pays de la Loire',
        'Picardie', 'Poitou-Charentes', 'Rhône-Alpes', 'Alsace', 'Corse',
        'Guadeloupe', 'Martinique', 'Guyane', 'Réunion', 'Mayotte',
        'PARIS', 'LYON', 'MARSEILLE', 'BORDEAUX', 'TOULOUSE', 'NANTES',
        'meteo_france', 'station_meteo_paris', 'SOL004', 'COT002', 'GRA005',
        'FERME001', 'VAL001', 'TRO003', 'Coopérative du Soleil Levant',
        'Ferme du Maïs d\'Argent - Maroc', 'Coopérative du Coton d\'Or - Maroc', 'Ferme des Grains - Maroc',
        'Ferme du Val - Maroc', 'Ferme des Trois Chênes - Maroc'
    ]
    
    # Mots-clés marocains à vérifier (pour confirmer la présence)
    mots_marocains = [
        'Maroc', 'Rabat', 'Casablanca', 'Fès', 'Marrakech', 'Agadir', 'Tanger',
        'Meknès', 'Oujda', 'Kénitra', 'Tétouan', 'Safi', 'El Jadida', 'Béni Mellal',
        'Taza', 'Larache', 'Khouribga', 'Ouarzazate', 'Dakhla', 'Laâyoune',
        'Tiflet', 'Sidi Slimane', 'Skhirate', 'Témara', 'Salé', 'Témara',
        'RABAT', 'CASABLANCA', 'FES', 'MARRAKECH', 'AGADIR', 'TANGER',
        'meteo_maroc', 'station_meteo_rabat', 'RABAT001', 'Mohammed Alami',
        'Ferme du Maïs d\'Argent - Maroc', 'Coopérative du Coton d\'Or - Maroc',
        'Ferme des Grains - Maroc', 'Ferme du Val - Maroc', 'Ferme des Trois Chênes - Maroc'
    ]
    
    # Recherche de tous les fichiers XML
    fichiers_xml = []
    for pattern in ['data/*.xml', 'views/*.xml']:
        fichiers_xml.extend(glob.glob(pattern))
    
    print(f"📁 Recherche dans {len(fichiers_xml)} fichiers XML...")
    print("-" * 60)
    
    total_references_francaises = 0
    total_references_marocaines = 0
    fichiers_problematiques = []
    fichiers_marocains = []
    
    for fichier in sorted(fichiers_xml):
        if os.path.exists(fichier):
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                references_francaises = []
                references_marocaines = []
                
                # Vérification des mots français
                for mot in mots_francais:
                    if mot in contenu:
                        references_francaises.append(mot)
                        total_references_francaises += 1
                
                # Vérification des mots marocains
                for mot in mots_marocains:
                    if mot in contenu:
                        references_marocaines.append(mot)
                        total_references_marocaines += 1
                
                # Affichage des résultats par fichier
                if references_francaises:
                    print(f"❌ {fichier}: {len(references_francaises)} références françaises")
                    fichiers_problematiques.append(fichier)
                    for ref in references_francaises[:3]:  # Afficher les 3 premières
                        print(f"   - {ref}")
                    if len(references_francaises) > 3:
                        print(f"   ... et {len(references_francaises) - 3} autres")
                elif references_marocaines:
                    print(f"✅ {fichier}: {len(references_marocaines)} références marocaines")
                    fichiers_marocains.append(fichier)
                else:
                    print(f"ℹ️  {fichier}: Aucune référence spécifique")
                    
            except Exception as e:
                print(f"❌ Erreur lors de la lecture de {fichier}: {e}")
    
    # Résumé final
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DE LA VÉRIFICATION FINALE")
    print("=" * 80)
    
    print(f"🔍 Fichiers analysés : {len(fichiers_xml)}")
    print(f"❌ Références françaises trouvées : {total_references_francaises}")
    print(f"✅ Références marocaines trouvées : {total_references_marocaines}")
    print(f"📁 Fichiers avec références françaises : {len(fichiers_problematiques)}")
    print(f"🇲🇦 Fichiers avec références marocaines : {len(fichiers_marocains)}")
    
    if total_references_francaises == 0:
        print(f"\n🎉 SUCCÈS TOTAL : Aucune référence française trouvée !")
        print("🇲🇦 Le module SmartAgriDecision est 100% marocain")
        print("✅ Prêt pour la production")
    else:
        print(f"\n⚠️  ATTENTION : {total_references_francaises} références françaises encore présentes")
        print("🔧 Fichiers nécessitant un nettoyage supplémentaire :")
        for fichier in fichiers_problematiques:
            print(f"   - {fichier}")
    
    # Création du rapport de vérification finale
    rapport_verification = f"""# RAPPORT DE VÉRIFICATION FINALE - SmartAgriDecision

## 📅 Date de la vérification finale
{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🔍 Résumé de la vérification finale
- **Fichiers analysés** : {len(fichiers_xml)}
- **Références françaises trouvées** : {total_references_francaises}
- **Références marocaines trouvées** : {total_references_marocaines}
- **Statut** : {'SUCCÈS TOTAL' if total_references_francaises == 0 else 'ATTENTION - Nettoyage nécessaire'}

## 📁 Fichiers avec références françaises
{chr(10).join([f"- {fichier}" for fichier in fichiers_problematiques]) if fichiers_problematiques else "- Aucun fichier problématique"}

## 🇲🇦 Fichiers avec références marocaines
{chr(10).join([f"- {fichier}" for fichier in fichiers_marocains]) if fichiers_marocains else "- Aucun fichier avec références marocaines"}

## 🎯 Résultat de la vérification finale
{'✅ SUCCÈS TOTAL : Le module est 100% marocain et prêt pour la production' if total_references_francaises == 0 else '⚠️ ATTENTION : Des références françaises persistent et nécessitent un nettoyage supplémentaire'}

## 🔧 Actions recommandées
{'1. Mettre à jour le module dans Odoo\n2. Vérifier l\'affichage dans l\'interface\n3. Tester les fonctionnalités marocaines\n4. Valider la suppression complète' if total_references_francaises == 0 else '1. Identifier la nature des références françaises restantes\n2. Effectuer un nettoyage ciblé\n3. Relancer la vérification\n4. Répéter jusqu\'à obtention du succès total'}

---
*Rapport généré automatiquement par le script de vérification finale*
"""
    
    with open("RAPPORT_VERIFICATION_FINALE.md", "w", encoding="utf-8") as f:
        f.write(rapport_verification)
    
    print(f"\n📋 Rapport de vérification finale créé : RAPPORT_VERIFICATION_FINALE.md")
    
    return total_references_francaises == 0

if __name__ == "__main__":
    try:
        verification_finale_maroc()
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution : {e}")
        import traceback
        traceback.print_exc()
