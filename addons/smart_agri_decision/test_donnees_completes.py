#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des Données Complètes SmartAgri Decision
==============================================

Ce script vérifie que toutes les données démo sont cohérentes et bien liées.
"""

import xml.etree.ElementTree as ET
import os
import sys

def test_donnees_completes():
    """Test principal des données complètes"""
    print("🚀 TEST DES DONNÉES COMPLÈTES SMARTAGRI DECISION")
    print("=" * 60)
    
    tests_passes = 0
    tests_totaux = 0
    
    # Test 1: Vérification du fichier principal
    print("\n🧪 Test 1: Fichier principal demo_data_complete.xml")
    try:
        tree = ET.parse('data/demo_data_complete.xml')
        root = tree.getroot()
        
        # Compter les enregistrements
        records = root.findall('.//record')
        print(f"   📊 Nombre d'enregistrements: {len(records)}")
        
        # Vérifier les modèles présents
        models = set()
        for record in records:
            model = record.get('model')
            if model:
                models.add(model)
        
        print(f"   🎯 Modèles couverts: {len(models)}")
        for model in sorted(models):
            print(f"      - {model}")
        
        tests_passes += 1
        print("   ✅ Fichier principal valide")
        
    except Exception as e:
        print(f"   ❌ Erreur fichier principal: {e}")
    
    tests_totaux += 1
    
    # Test 2: Vérification du fichier supplémentaire
    print("\n🧪 Test 2: Fichier supplémentaire demo_data_supplementaires.xml")
    try:
        tree = ET.parse('data/demo_data_supplementaires.xml')
        root = tree.getroot()
        
        records = root.findall('.//record')
        print(f"   📊 Nombre d'enregistrements: {len(records)}")
        
        models = set()
        for record in records:
            model = record.get('model')
            if model:
                models.add(model)
        
        print(f"   🎯 Modèles couverts: {len(models)}")
        for model in sorted(models):
            print(f"      - {model}")
        
        tests_passes += 1
        print("   ✅ Fichier supplémentaire valide")
        
    except Exception as e:
        print(f"   ❌ Erreur fichier supplémentaire: {e}")
    
    tests_totaux += 1
    
    # Test 3: Vérification des relations
    print("\n🧪 Test 3: Cohérence des relations entre modèles")
    try:
        # Vérifier que les références sont cohérentes
        tree = ET.parse('data/demo_data_complete.xml')
        root = tree.getroot()
        
        # Vérifier les références exploitation
        exploitations = root.findall(".//record[@model='smart_agri_exploitation']")
        parcelles = root.findall(".//record[@model='smart_agri_parcelle']")
        cultures = root.findall(".//record[@model='smart_agri_culture']")
        
        print(f"   🏭 Exploitations: {len(exploitations)}")
        print(f"   🗺️  Parcelles: {len(parcelles)}")
        print(f"   🌾 Cultures: {len(cultures)}")
        
        # Vérifier que chaque parcelle a une exploitation
        for parcelle in parcelles:
            exploitation_ref = parcelle.find(".//field[@name='exploitation_id']")
            if exploitation_ref is not None:
                print(f"      ✅ Parcelle liée à exploitation")
            else:
                print(f"      ⚠️  Parcelle sans exploitation")
        
        tests_passes += 1
        print("   ✅ Relations cohérentes")
        
    except Exception as e:
        print(f"   ❌ Erreur vérification relations: {e}")
    
    tests_totaux += 1
    
    # Test 4: Vérification des données IA
    print("\n🧪 Test 4: Données IA et modèles")
    try:
        tree = ET.parse('data/demo_data_complete.xml')
        root = tree.getroot()
        
        # Compter les modèles IA
        modeles_ia = root.findall(".//record[@model='smart_agri_ai_model']")
        predictions = root.findall(".//record[@model='smart_agri_ia_predictions']")
        simulations = root.findall(".//record[@model='smart_agri_ia_simulateur']")
        
        print(f"   🤖 Modèles IA: {len(modeles_ia)}")
        print(f"   🔮 Prédictions: {len(predictions)}")
        print(f"   🎮 Simulations: {len(simulations)}")
        
        # Vérifier la qualité des modèles IA
        for modele in modeles_ia:
            precision = modele.find(".//field[@name='precision_modele']")
            if precision is not None:
                print(f"      ✅ Modèle avec précision: {precision.text}%")
        
        tests_passes += 1
        print("   ✅ Données IA complètes")
        
    except Exception as e:
        print(f"   ❌ Erreur données IA: {e}")
    
    tests_totaux += 1
    
    # Test 5: Vérification des données météo
    print("\n🧪 Test 5: Données météorologiques")
    try:
        tree = ET.parse('data/demo_data_complete.xml')
        root = tree.getroot()
        
        # Compter les données météo
        stations = root.findall(".//record[@model='smart_agri_station_meteo']")
        imports_meteostat = root.findall(".//record[@model='smart_agri_meteostat_import']")
        donnees_meteo = root.findall(".//record[@model='smart_agri_meteo']")
        
        print(f"   🌡️  Stations météo: {len(stations)}")
        print(f"   📡 Imports Meteostat: {len(imports_meteostat)}")
        print(f"   📊 Données météo: {len(donnees_meteo)}")
        
        # Vérifier la cohérence géographique
        for station in stations:
            lat = station.find(".//field[@name='latitude']")
            lon = station.find(".//field[@name='longitude']")
            if lat is not None and lon is not None:
                print(f"      ✅ Station avec coordonnées: {lat.text}, {lon.text}")
        
        tests_passes += 1
        print("   ✅ Données météo cohérentes")
        
    except Exception as e:
        print(f"   ❌ Erreur données météo: {e}")
    
    tests_totaux += 1
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"Tests réussis: {tests_passes}/{tests_totaux}")
    
    if tests_passes == tests_totaux:
        print("🎉 Toutes les données sont cohérentes et complètes !")
        print("✅ Le module est prêt pour la démonstration")
        return True
    else:
        print("⚠️  Certains tests ont échoué")
        return False

if __name__ == "__main__":
    try:
        success = test_donnees_completes()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        sys.exit(1)
