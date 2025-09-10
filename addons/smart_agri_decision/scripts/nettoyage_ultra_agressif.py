#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NETTOYAGE ULTRA-AGRESSIF - ÉLIMINATION DÉFINITIVE DES DONNÉES FRANÇAISES
Script de nettoyage radical pour forcer la suppression de toutes les références françaises
"""

import os
import re
import glob
from pathlib import Path

def nettoyage_ultra_agressif():
    """Nettoyage ultra-agressif de toutes les données françaises"""
    
    print("🔥 NETTOYAGE ULTRA-AGRESSIF - ÉLIMINATION DÉFINITIVE")
    print("=" * 60)
    
    # Patterns français à éliminer définitivement
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
    
    # Patterns spécifiques à éliminer
    patterns_specifiques = [
        r'station_meteo_paris',
        r'PARIS001',
        r'meteo_france',
        r'Ferme du Maïs d\'Argent',
        r'nord-ouest'
    ]
    
    # Combiner tous les patterns
    tous_patterns = patterns_francais + patterns_specifiques
    
    # Fichiers à traiter
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
    
    total_remplacements = 0
    
    for fichier in fichiers_xml:
        if os.path.exists(fichier):
            print(f"\n🔍 Traitement de {fichier}...")
            
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                contenu_original = contenu
                remplacements_fichier = 0
                
                # Remplacer tous les patterns français
                for pattern in tous_patterns:
                    # Compter les occurrences
                    occurrences = len(re.findall(pattern, contenu, re.IGNORECASE))
                    if occurrences > 0:
                        print(f"   ⚠️  {occurrences} occurrence(s) de '{pattern}' trouvée(s)")
                        
                        # Remplacer par des valeurs marocaines
                        if 'paris' in pattern.lower():
                            remplacement = 'rabat'
                        elif 'france' in pattern.lower():
                            remplacement = 'maroc'
                        elif 'station_meteo_paris' in pattern.lower():
                            remplacement = 'station_meteo_rabat'
                        elif 'meteo_france' in pattern.lower():
                            remplacement = 'meteo_maroc'
                        elif 'Ferme du Maïs d\'Argent' in pattern:
                            remplacement = 'Ferme du Maïs d\'Argent - Maroc'
                        elif 'nord-ouest' in pattern.lower():
                            remplacement = 'Nord'
                        else:
                            remplacement = 'maroc'
                        
                        contenu = re.sub(pattern, remplacement, contenu, flags=re.IGNORECASE)
                        remplacements_fichier += occurrences
                
                # Si des changements ont été faits, sauvegarder
                if contenu != contenu_original:
                    with open(fichier, 'w', encoding='utf-8') as f:
                        f.write(contenu)
                    
                    print(f"   ✅ {remplacements_fichier} remplacement(s) effectué(s)")
                    total_remplacements += remplacements_fichier
                else:
                    print(f"   ✅ Aucun changement nécessaire")
                    
            except Exception as e:
                print(f"   ❌ Erreur lors du traitement: {e}")
        else:
            print(f"   ⚠️  Fichier {fichier} non trouvé")
    
    print(f"\n🎯 RÉSUMÉ DU NETTOYAGE ULTRA-AGRESSIF")
    print("=" * 50)
    print(f"Total des remplacements: {total_remplacements}")
    
    if total_remplacements > 0:
        print("🔥 NETTOYAGE TERMINÉ - REDÉMARRAGE D'ODOO REQUIS")
        print("⚠️  IMPORTANT: Redémarrez Odoo pour appliquer les changements!")
    else:
        print("✅ Aucune donnée française trouvée - Nettoyage terminé")

if __name__ == "__main__":
    nettoyage_ultra_agressif()
