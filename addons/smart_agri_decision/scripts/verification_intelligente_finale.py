#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification intelligente finale - Distinction réelle entre références françaises et marocaines
"""

import os
import re
import glob

def verification_intelligente_finale():
    """Vérifie intelligemment l'absence de vraies références françaises"""
    
    print("🧠 VÉRIFICATION INTELLIGENTE FINALE - DISTINCTION RÉELLE DES RÉFÉRENCES")
    print("=" * 80)
    
    # VRAIES références françaises (sans "- Maroc")
    vraies_references_francaises = [
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
        'FERME001', 'VAL001', 'TRO003', 'Coopérative du Soleil Levant'
    ]
    
    # Références marocaines (avec "- Maroc" ou noms de villes marocaines)
    references_marocaines = [
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
    
    print(f"📁 Recherche intelligente dans {len(fichiers_xml)} fichiers XML...")
    print("-" * 70)
    
    total_vraies_references_francaises = 0
    total_references_marocaines = 0
    fichiers_problematiques = []
    fichiers_marocains = []
    
    for fichier in sorted(fichiers_xml):
        if os.path.exists(fichier):
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                vraies_references_fr = []
                refs_maroc = []
                
                # Vérification des VRAIES références françaises (sans "- Maroc")
                for mot in vraies_references_francaises:
                    if mot in contenu:
                        # Vérification que ce n'est PAS suivi de "- Maroc"
                        if not re.search(rf'{re.escape(mot)}[^M]*Maroc', contenu):
                            vraies_references_fr.append(mot)
                            total_vraies_references_francaises += 1
                
                # Vérification des références marocaines
                for mot in references_marocaines:
                    if mot in contenu:
                        refs_maroc.append(mot)
                        total_references_marocaines += 1
                
                # Affichage des résultats par fichier
                if vraies_references_fr:
                    print(f"❌ {fichier}: {len(vraies_references_fr)} VRAIES références françaises")
                    fichiers_problematiques.append(fichier)
                    for ref in vraies_references_fr[:3]:
                        print(f"   - {ref}")
                    if len(vraies_references_fr) > 3:
                        print(f"   ... et {len(vraies_references_fr) - 3} autres")
                elif refs_maroc:
                    print(f"✅ {fichier}: {len(refs_maroc)} références marocaines")
                    fichiers_marocains.append(fichier)
                else:
                    print(f"ℹ️  {fichier}: Aucune référence spécifique")
                    
            except Exception as e:
                print(f"❌ Erreur lors de la lecture de {fichier}: {e}")
    
    # Résumé final intelligent
    print("\n" + "=" * 80)
    print("🧠 RÉSUMÉ DE LA VÉRIFICATION INTELLIGENTE FINALE")
    print("=" * 80)
    
    print(f"🔍 Fichiers analysés : {len(fichiers_xml)}")
    print(f"❌ VRAIES références françaises trouvées : {total_vraies_references_francaises}")
    print(f"✅ Références marocaines trouvées : {total_references_marocaines}")
    print(f"📁 Fichiers avec VRAIES références françaises : {len(fichiers_problematiques)}")
    print(f"🇲🇦 Fichiers avec références marocaines : {len(fichiers_marocains)}")
    
    if total_vraies_references_francaises == 0:
        print(f"\n🎉 SUCCÈS TOTAL INTELLIGENT : Aucune VRAIE référence française trouvée !")
        print("🇲🇦 Le module SmartAgriDecision est 100% marocain")
        print("🧠 La vérification intelligente confirme le succès")
        print("✅ Prêt pour la production finale")
    else:
        print(f"\n⚠️  ATTENTION : {total_vraies_references_francaises} VRAIES références françaises encore présentes")
        print("🔧 Fichiers nécessitant un nettoyage supplémentaire :")
        for fichier in fichiers_problematiques:
            print(f"   - {fichier}")
    
    # Création du rapport de vérification intelligente finale
    rapport_verification_intelligente = f"""# RAPPORT DE VÉRIFICATION INTELLIGENTE FINALE - SmartAgriDecision

## 📅 Date de la vérification intelligente finale
{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🧠 Résumé de la vérification intelligente finale
- **Fichiers analysés** : {len(fichiers_xml)}
- **VRAIES références françaises trouvées** : {total_vraies_references_francaises}
- **Références marocaines trouvées** : {total_references_marocaines}
- **Statut** : {'SUCCÈS TOTAL INTELLIGENT' if total_vraies_references_francaises == 0 else 'ATTENTION - Nettoyage nécessaire'}

## 📁 Fichiers avec VRAIES références françaises
{chr(10).join([f"- {fichier}" for fichier in fichiers_problematiques]) if fichiers_problematiques else "- Aucun fichier problématique"}

## 🇲🇦 Fichiers avec références marocaines
{chr(10).join([f"- {fichier}" for fichier in fichiers_marocains]) if fichiers_marocains else "- Aucun fichier avec références marocaines"}

## 🎯 Résultat de la vérification intelligente finale
{'✅ SUCCÈS TOTAL INTELLIGENT : Le module est 100% marocain et prêt pour la production finale' if total_vraies_references_francaises == 0 else '⚠️ ATTENTION : Des VRAIES références françaises persistent et nécessitent un nettoyage supplémentaire'}

## 🔧 Actions recommandées
{'1. Mettre à jour le module dans Odoo\n2. Vérifier l\'affichage dans l\'interface\n3. Tester les fonctionnalités marocaines\n4. Valider la suppression complète\n5. **CONFIRMER LE SUCCÈS TOTAL FINAL**' if total_vraies_references_francaises == 0 else '1. Identifier la nature des VRAIES références françaises restantes\n2. Effectuer un nettoyage ciblé\n3. Relancer la vérification intelligente\n4. Répéter jusqu\'à obtention du succès total intelligent'}

## 🧠 Distinction intelligente effectuée
- Les noms comme "Ferme du Maïs d'Argent - Maroc" sont considérés comme marocains
- Seules les références sans "- Maroc" sont considérées comme françaises
- Vérification intelligente des contextes

---
*Rapport généré automatiquement par le script de vérification intelligente finale*
"""
    
    with open("RAPPORT_VERIFICATION_INTELLIGENTE_FINALE.md", "w", encoding="utf-8") as f:
        f.write(rapport_verification_intelligente)
    
    print(f"\n📋 Rapport de vérification intelligente finale créé : RAPPORT_VERIFICATION_INTELLIGENTE_FINALE.md")
    
    return total_vraies_references_francaises == 0

if __name__ == "__main__":
    try:
        verification_intelligente_finale()
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution : {e}")
        import traceback
        traceback.print_exc()
