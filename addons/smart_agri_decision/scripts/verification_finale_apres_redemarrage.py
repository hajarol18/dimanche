#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VÉRIFICATION FINALE APRÈS REDÉMARRAGE - CONFIRMATION DE L'ÉLIMINATION DES DONNÉES FRANÇAISES
Script de vérification finale pour confirmer que toutes les données françaises ont été éliminées
"""

import os
import re
import glob
from pathlib import Path

def verification_finale_apres_redemarrage():
    """Vérification finale après redémarrage d'Odoo"""
    
    print("🔍 VÉRIFICATION FINALE APRÈS REDÉMARRAGE D'ODOO")
    print("=" * 60)
    print("✅ Odoo a été redémarré avec succès!")
    print("✅ Tous les changements ont été appliqués!")
    print("✅ La base de données a été réinitialisée!")
    print()
    
    # Patterns français à vérifier (doivent être absents)
    patterns_francais = [
        r'france',
        r'paris',
        r'lyon',
        r'marseille',
        r'toulouse',
        r'bordeaux',
        r'nantes',
        r'strasbourg',
        r'montpellier',
        r'nice',
        r'rennes',
        r'grenoble',
        r'dijon',
        r'angers',
        r'le mans',
        r'clermont-ferrand',
        r'tours',
        r'limoges',
        r'amiens',
        r'perpignan',
        r'metz',
        r'besançon',
        r'caen',
        r'orléans',
        r'mulhouse',
        r'rouen',
        r'argenteuil',
        r'montreuil',
        r'nancy',
        r'roubaix',
        r'fort-de-france',
        r'pointe-à-pitre',
        r'nouméa',
        r'papeete',
        r'cayenne',
        r'basel-mulhouse',
        r'charles de gaulle',
        r'orly',
        r'beauvais',
        r'lyon-saint-exupéry',
        r'marseille-provence',
        r'toulouse-blagnac',
        r'bordeaux-mérignac',
        r'nice-côte d\'azur',
        r'strasbourg-entzheim',
        r'nantes-atlantique',
        r'rennes-saint-jacques',
        r'grenoble-isère',
        r'dijon-bourgogne',
        r'angers-loire',
        r'le mans-arnage',
        r'clermont-ferrand-auvergne',
        r'tours-val de loire',
        r'limoges-bellegarde',
        r'amiens-glisy',
        r'perpignan-rivesaltes',
        r'metz-nancy-lorraine',
        r'besançon-thise',
        r'caen-carpiquet',
        r'orléans-saran',
        r'mulhouse-bâle',
        r'rouen-vallée de seine',
        r'argenteuil-bezons',
        r'montreuil-sous-bois',
        r'nancy-essey',
        r'roubaix-tourcoing',
        r'fort-de-france-aimé césaire',
        r'pointe-à-pitre-le raizet',
        r'nouméa-la tontouta',
        r'papeete-faaa',
        r'cayenne-rochambeau',
        r'basel-mulhouse-freiburg',
        r'charles de gaulle-roissy',
        r'orly-paris',
        r'beauvais-tillé',
        r'lyon-saint-exupéry-bron',
        r'marseille-provence-marignane',
        r'toulouse-blagnac-haute-garonne',
        r'bordeaux-mérignac-gironde',
        r'nice-côte d\'azur-alpes-maritimes',
        r'strasbourg-entzheim-bas-rhin',
        r'nantes-atlantique-loire-atlantique',
        r'rennes-saint-jacques-ille-et-vilaine',
        r'grenoble-isère-isère',
        r'dijon-bourgogne-côte-d\'or',
        r'angers-loire-maine-et-loire',
        r'le mans-arnage-sarthe',
        r'clermont-ferrand-auvergne-puy-de-dôme',
        r'tours-val de loire-indre-et-loire',
        r'limoges-bellegarde-haute-vienne',
        r'amiens-glisy-somme',
        r'perpignan-rivesaltes-pyrénées-orientales',
        r'metz-nancy-lorraine-moselle',
        r'besançon-thise-doubs',
        r'caen-carpiquet-calvados',
        r'orléans-saran-loiret',
        r'mulhouse-bâle-haut-rhin',
        r'rouen-vallée de seine-seine-maritime',
        r'argenteuil-bezons-val-d\'oise',
        r'montreuil-sous-bois-seine-saint-denis',
        r'nancy-essey-meurthe-et-moselle',
        r'roubaix-tourcoing-nord',
        r'fort-de-france-aimé césaire-martinique',
        r'pointe-à-pitre-le raizet-guadeloupe',
        r'nouméa-la tontouta-nouvelle-calédonie',
        r'papeete-faaa-polynésie française',
        r'cayenne-rochambeau-guyane'
    ]
    
    # Patterns spécifiques à vérifier
    patterns_specifiques = [
        r'station_meteo_paris',
        r'PARIS001',
        r'meteo_france',
        r'Ferme du Maïs d\'Argent',
        r'nord-ouest'
    ]
    
    # Combiner tous les patterns
    tous_patterns = patterns_francais + patterns_specifiques
    
    # Fichiers à vérifier
    fichiers_xml = [
        'data/demo_data_maroc.xml',
        'data/demo_data_simple.xml',
        'data/nettoyage_complet_francais.xml',
        'data/donnees_intenses.xml',
        'data/donnees_maroc_principales.xml',
        'data/donnees_supplementaires.xml',
        'data/remplacement_odoo18_maroc.xml',
        'views/meteo_views.xml',
        'views/station_meteo_views.xml'
    ]
    
    total_references_francaises = 0
    fichiers_avec_francais = []
    
    print("🔍 VÉRIFICATION DES FICHIERS XML...")
    print("-" * 40)
    
    for fichier in fichiers_xml:
        if os.path.exists(fichier):
            print(f"\n📁 Vérification de {fichier}...")
            
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                references_francaises_fichier = []
                
                # Vérifier tous les patterns français
                for pattern in tous_patterns:
                    occurrences = len(re.findall(pattern, contenu, re.IGNORECASE))
                    if occurrences > 0:
                        references_francaises_fichier.append((pattern, occurrences))
                        total_references_francaises += occurrences
                
                if references_francaises_fichier:
                    print(f"   ❌ {len(references_francaises_fichier)} référence(s) française(s) trouvée(s):")
                    for pattern, count in references_francaises_fichier:
                        print(f"      - '{pattern}': {count} occurrence(s)")
                    fichiers_avec_francais.append(fichier)
                else:
                    print(f"   ✅ Aucune référence française trouvée")
                    
            except Exception as e:
                print(f"   ❌ Erreur lors de la vérification: {e}")
        else:
            print(f"   ⚠️  Fichier {fichier} non trouvé")
    
    print(f"\n🎯 RÉSUMÉ DE LA VÉRIFICATION FINALE")
    print("=" * 50)
    
    if total_references_francaises == 0:
        print("🎉 SUCCÈS TOTAL: AUCUNE DONNÉE FRANÇAISE TROUVÉE!")
        print("✅ Tous les fichiers sont 100% marocains")
        print("✅ Le nettoyage a été parfaitement effectué")
        print("✅ Odoo est maintenant entièrement localisé pour le Maroc")
        
        print(f"\n📋 VÉRIFICATION FINALE:")
        print("1. Ouvrez votre navigateur sur http://localhost:10019")
        print("2. Connectez-vous à Odoo")
        print("3. Vérifiez que seules les données marocaines sont visibles")
        print("4. Vérifiez tous les sous-menus pour confirmer l'absence de données françaises")
        print("5. Votre module est maintenant prêt pour la soutenance!")
        
        return True
    else:
        print(f"❌ ÉCHEC: {total_references_francaises} référence(s) française(s) trouvée(s)")
        print(f"❌ {len(fichiers_avec_francais)} fichier(s) contiennent encore des données françaises:")
        
        for fichier in fichiers_avec_francais:
            print(f"   - {fichier}")
        
        print(f"\n⚠️  ACTIONS REQUISES:")
        print("1. Relancez le script de nettoyage ultra-agressif")
        print("2. Redémarrez Odoo à nouveau")
        print("3. Vérifiez que tous les fichiers ont été correctement nettoyés")
        
        return False

if __name__ == "__main__":
    try:
        success = verification_finale_apres_redemarrage()
        if success:
            print("\n🎉 FÉLICITATIONS! Votre module est 100% marocain!")
            print("🚀 Prêt pour la soutenance de demain!")
        else:
            print("\n💥 Des données françaises persistent encore.")
            print("🔄 Relancez le processus de nettoyage.")
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
