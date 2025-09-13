#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WORKFLOW OPTIMAL - IMPORT METEOSTAT
La meilleure façon d'utiliser l'import Meteostat avec les exploitations
"""

import xmlrpc.client
from datetime import datetime, timedelta

def workflow_meteostat_optimal():
    """Workflow optimal pour l'import Meteostat"""
    
    print("🎯 WORKFLOW OPTIMAL - IMPORT METEOSTAT")
    print("=" * 50)
    
    # Configuration de connexion
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if not uid:
            print("❌ Échec de l'authentification")
            return False
        
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        print("✅ Connexion réussie à Odoo")
        
        # ÉTAPE 1: Vérifier/Créer les exploitations avec géolocalisation
        print("\n🏭 ÉTAPE 1: Préparer les exploitations...")
        
        exploitations = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'search_read', 
                                        [[]], {'fields': ['id', 'name', 'latitude', 'longitude', 'region']})
        
        if not exploitations:
            print("❌ Aucune exploitation trouvée. Créons des exploitations marocaines...")
            
            # Créer des exploitations marocaines avec géolocalisation
            exploitations_maroc = [
                {
                    'name': 'Exploitation Casablanca - Céréales',
                    'region': 'Casablanca-Settat',
                    'surface_totale': 150.0,
                    'latitude': 33.5731,
                    'longitude': -7.5898,
                    'type_exploitation': 'cereales'
                },
                {
                    'name': 'Exploitation Rabat - Arboriculture',
                    'region': 'Rabat-Salé-Kénitra',
                    'surface_totale': 80.0,
                    'latitude': 34.0209,
                    'longitude': -6.8416,
                    'type_exploitation': 'arboriculture'
                },
                {
                    'name': 'Exploitation Marrakech - Maraîchage',
                    'region': 'Marrakech-Safi',
                    'surface_totale': 120.0,
                    'latitude': 31.6295,
                    'longitude': -7.9811,
                    'type_exploitation': 'maraichage'
                }
            ]
            
            for exp_data in exploitations_maroc:
                exp_id = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'create', [exp_data])
                print(f"✅ Exploitation créée: {exp_data['name']} (ID: {exp_id})")
            
            # Récupérer les exploitations créées
            exploitations = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'search_read', 
                                            [[]], {'fields': ['id', 'name', 'latitude', 'longitude', 'region']})
        
        print(f"✅ {len(exploitations)} exploitations disponibles")
        
        # ÉTAPE 2: Créer des imports Meteostat pour chaque exploitation
        print("\n📡 ÉTAPE 2: Créer les imports Meteostat...")
        
        # Stations météo marocaines
        stations_maroc = {
            'CASA001': {'name': 'Casablanca', 'lat': 33.5731, 'lon': -7.5898},
            'RABAT001': {'name': 'Rabat', 'lat': 34.0209, 'lon': -6.8416},
            'MARRAK001': {'name': 'Marrakech', 'lat': 31.6295, 'lon': -7.9811}
        }
        
        imports_crees = []
        
        for i, exploitation in enumerate(exploitations):
            # Sélectionner la station la plus proche
            station_id = list(stations_maroc.keys())[i % len(stations_maroc)]
            station = stations_maroc[station_id]
            
            # Créer l'import Meteostat
            import_data = {
                'name': f'Import Meteostat - {exploitation["name"]}',
                'exploitation_id': exploitation['id'],
                'station_id': station_id,
                'latitude': station['lat'],
                'longitude': station['lon'],
                'date_debut': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'date_fin': datetime.now().strftime('%Y-%m-%d'),
                'api_key': 'demo_key'
            }
            
            import_id = models.execute_kw(db, uid, password, 'smart_agri_meteostat_enhanced', 'create', [import_data])
            imports_crees.append(import_id)
            print(f"✅ Import créé pour {exploitation['name']} (ID: {import_id})")
        
        # ÉTAPE 3: Lancer tous les imports
        print("\n🚀 ÉTAPE 3: Lancer tous les imports...")
        
        for import_id in imports_crees:
            try:
                result = models.execute_kw(db, uid, password, 'smart_agri_meteostat_enhanced', 'action_importer_donnees_reelles', [import_id])
                print(f"✅ Import {import_id} lancé")
            except Exception as e:
                print(f"⚠️ Erreur import {import_id}: {str(e)}")
        
        # ÉTAPE 4: Vérifier les résultats
        print("\n📊 ÉTAPE 4: Vérifier les résultats...")
        
        import time
        time.sleep(5)  # Attendre le traitement
        
        for import_id in imports_crees:
            import_result = models.execute_kw(db, uid, password, 'smart_agri_meteostat_enhanced', 'read', [import_id], 
                                           ['exploitation_id', 'statut_import', 'nombre_enregistrements', 'log_import'])
            
            if import_result:
                result = import_result[0]
                print(f"📡 Import {import_id}: {result.get('statut_import', 'N/A')} - {result.get('nombre_enregistrements', 0)} enregistrements")
        
        # ÉTAPE 5: Vérifier les données météo par exploitation
        print("\n🌤️ ÉTAPE 5: Vérifier les données météo par exploitation...")
        
        for exploitation in exploitations:
            meteo_count = models.execute_kw(db, uid, password, 'smart_agri_meteo', 'search_count', 
                                          [[('exploitation_id', '=', exploitation['id'])]])
            print(f"🌡️ {exploitation['name']}: {meteo_count} données météo")
            
            if meteo_count > 0:
                # Récupérer les dernières données
                meteo_data = models.execute_kw(db, uid, password, 'smart_agri_meteo', 'search_read', 
                                             [[('exploitation_id', '=', exploitation['id'])]], 
                                             {'fields': ['date_mesure', 'temperature', 'precipitation', 'source']}, 
                                             limit=3, order='date_mesure desc')
                
                for meteo in meteo_data:
                    print(f"  📅 {meteo['date_mesure']}: {meteo['temperature']}°C, {meteo['precipitation']}mm ({meteo['source']})")
        
        # ÉTAPE 6: Créer des analyses IA pour chaque exploitation
        print("\n🤖 ÉTAPE 6: Créer des analyses IA...")
        
        for exploitation in exploitations:
            # Créer une analyse IA de prédiction de rendement
            analyse_data = {
                'name': f'Analyse IA - {exploitation["name"]}',
                'exploitation_id': exploitation['id'],
                'type_analyse': 'prediction_rendement'
            }
            
            analyse_id = models.execute_kw(db, uid, password, 'smart_agri_ia_enhanced', 'create', [analyse_data])
            
            # Lancer l'analyse
            try:
                result = models.execute_kw(db, uid, password, 'smart_agri_ia_enhanced', 'action_lancer_analyse_ia', [analyse_id])
                print(f"✅ Analyse IA créée pour {exploitation['name']} (ID: {analyse_id})")
            except Exception as e:
                print(f"⚠️ Erreur analyse IA {exploitation['name']}: {str(e)}")
        
        print("\n🎉 WORKFLOW OPTIMAL TERMINÉ !")
        print("\n📍 RÉSULTATS DISPONIBLES:")
        print("1. Menu '🌤️ Météo & Climat' > '📡 Meteostat Réel'")
        print("2. Menu '🌤️ Météo & Climat' > '🌡️ Données Météo'")
        print("3. Menu '🤖 Intelligence Artificielle' > '🚀 IA Avancée'")
        print("4. Menu '📊 Gestion des Données' > '🏡 Exploitations'")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

if __name__ == "__main__":
    workflow_meteostat_optimal()
