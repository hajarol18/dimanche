#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xmlrpc.client
import random
from datetime import datetime, timedelta

def fill_all_climate_menus():
    """Remplir TOUS les sous-menus climat avec des données complètes"""
    
    # Configuration Odoo
    url = 'http://localhost:10020'
    db = 'odoo123'
    username = 'hajar'
    password = 'hajar'
    
    print("🌤️ REMPLISSAGE COMPLET DE TOUS LES SOUS-MENUS CLIMAT")
    print("=" * 60)
    
    try:
        # Connexion
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if not uid:
            print("❌ Échec connexion Odoo")
            return
            
        print("✅ Connexion Odoo réussie")
        
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # Récupérer l'exploitation
        exploitation_ids = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'search', [[]])
        exploitation_id = exploitation_ids[0] if exploitation_ids else None
        print(f"✅ Exploitation trouvée: ID {exploitation_id}")
        
        # 1. REMPLIR DONNÉES MÉTÉO (20 enregistrements)
        print("\n🌡️ AJOUT DE 20 DONNÉES MÉTÉO...")
        print("-" * 40)
        
        for i in range(20):
            date_mesure = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            meteo_data = {
                'name': f'Mesure météo {i+1} - {date_mesure}',
                'description': f'Données météorologiques complètes du {date_mesure}',
                'exploitation_id': exploitation_id,
                'date_mesure': date_mesure,
                'temperature': round(random.uniform(15, 35), 1),
                'temperature_min': round(random.uniform(10, 25), 1),
                'temperature_max': round(random.uniform(25, 40), 1),
                'precipitation': round(random.uniform(0, 50), 1),
                'humidite': round(random.uniform(30, 80), 1),
                'vitesse_vent': round(random.uniform(5, 25), 1),
                'direction_vent': random.choice(['nord', 'sud', 'est', 'ouest', 'nord_est', 'sud_ouest']),
                'pression_atmospherique': round(random.uniform(1000, 1020), 1),
                'rayonnement_solaire': round(random.uniform(200, 800), 1),
                'indice_uv': round(random.uniform(1, 10), 1)
            }
            
            try:
                meteo_id = models.execute_kw(db, uid, password, 'smart_agri_meteo', 'create', [meteo_data])
                print(f"  ✅ Données météo {i+1} créées (ID: {meteo_id})")
            except Exception as e:
                print(f"  ❌ Erreur météo {i+1}: {str(e)[:50]}")
        
        # 2. REMPLIR SCÉNARIOS CLIMATIQUES (5 enregistrements)
        print("\n🌍 AJOUT DE 5 SCÉNARIOS CLIMATIQUES...")
        print("-" * 40)
        
        scenarios = [
            {
                'name': 'Scénario Optimiste 2030',
                'description': 'Scénario optimiste pour 2030 avec réduction des émissions',
                'exploitation_id': exploitation_id,
                'type_scenario': 'optimiste',
                'periode_debut': '2024-01-01',
                'periode_fin': '2030-12-31',
                'rechauffement_attendu': 1.5,
                'impact_rendement': 'positif',
                'probabilite': 30.0,
                'etat': 'actif'
            },
            {
                'name': 'Scénario Modéré 2050',
                'description': 'Scénario modéré pour 2050 avec stabilisation',
                'exploitation_id': exploitation_id,
                'type_scenario': 'modere',
                'periode_debut': '2024-01-01',
                'periode_fin': '2050-12-31',
                'rechauffement_attendu': 2.0,
                'impact_rendement': 'neutre',
                'probabilite': 50.0,
                'etat': 'actif'
            },
            {
                'name': 'Scénario Pessimiste 2100',
                'description': 'Scénario pessimiste pour 2100 sans action',
                'exploitation_id': exploitation_id,
                'type_scenario': 'pessimiste',
                'periode_debut': '2024-01-01',
                'periode_fin': '2100-12-31',
                'rechauffement_attendu': 4.0,
                'impact_rendement': 'negatif',
                'probabilite': 20.0,
                'etat': 'actif'
            },
            {
                'name': 'Scénario Sécheresse 2025',
                'description': 'Scénario de sécheresse pour 2025',
                'exploitation_id': exploitation_id,
                'type_scenario': 'secheresse',
                'periode_debut': '2025-01-01',
                'periode_fin': '2025-12-31',
                'rechauffement_attendu': 2.5,
                'impact_rendement': 'negatif',
                'probabilite': 15.0,
                'etat': 'actif'
            },
            {
                'name': 'Scénario Pluvieux 2026',
                'description': 'Scénario pluvieux pour 2026',
                'exploitation_id': exploitation_id,
                'type_scenario': 'pluvieux',
                'periode_debut': '2026-01-01',
                'periode_fin': '2026-12-31',
                'rechauffement_attendu': 1.0,
                'impact_rendement': 'positif',
                'probabilite': 25.0,
                'etat': 'actif'
            }
        ]
        
        for scenario in scenarios:
            try:
                scenario_id = models.execute_kw(db, uid, password, 'smart_agri_scenario_climatique', 'create', [scenario])
                print(f"  ✅ Scénario créé: {scenario['name']} (ID: {scenario_id})")
            except Exception as e:
                print(f"  ❌ Erreur scénario: {str(e)[:50]}")
        
        # 3. REMPLIR ALERTES CLIMATIQUES (10 enregistrements)
        print("\n⚠️ AJOUT DE 10 ALERTES CLIMATIQUES...")
        print("-" * 40)
        
        types_alertes = ['secheresse', 'canicule', 'gel', 'inondation', 'vent_fort', 'grele', 'humidite_faible']
        niveaux = ['jaune', 'orange', 'rouge']
        
        for i in range(10):
            alerte_data = {
                'name': f'Alerte {i+1} - {random.choice(types_alertes).title()}',
                'description': f'Description détaillée de l\'alerte {i+1}',
                'exploitation_id': exploitation_id,
                'type_alerte': random.choice(types_alertes),
                'niveau': random.choice(niveaux),
                'date_detection': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
                'date_debut': (datetime.now() - timedelta(days=random.randint(0, 10))).strftime('%Y-%m-%d'),
                'date_fin': (datetime.now() + timedelta(days=random.randint(1, 15))).strftime('%Y-%m-%d'),
                'temperature_actuelle': round(random.uniform(20, 40), 1),
                'precipitation_7j': round(random.uniform(0, 100), 1),
                'recommandations': f'Recommandations pour l\'alerte {i+1}'
            }
            
            try:
                alerte_id = models.execute_kw(db, uid, password, 'smart_agri_alerte_climatique', 'create', [alerte_data])
                print(f"  ✅ Alerte {i+1} créée (ID: {alerte_id})")
            except Exception as e:
                print(f"  ❌ Erreur alerte {i+1}: {str(e)[:50]}")
        
        # 4. REMPLIR TENDANCES CLIMATIQUES (8 enregistrements)
        print("\n📈 AJOUT DE 8 TENDANCES CLIMATIQUES...")
        print("-" * 40)
        
        for i in range(8):
            periode_debut = (datetime.now() - timedelta(days=30*i)).strftime('%Y-%m-%d')
            periode_fin = (datetime.now() - timedelta(days=30*i-30)).strftime('%Y-%m-%d')
            
            tendance_data = {
                'name': f'Tendance {i+1} - Période {periode_debut} à {periode_fin}',
                'description': f'Analyse des tendances climatiques pour la période {i+1}',
                'exploitation_id': exploitation_id,
                'periode_debut': periode_debut,
                'periode_fin': periode_fin,
                'temperature_moyenne': round(random.uniform(20, 30), 1),
                'temperature_max': round(random.uniform(30, 40), 1),
                'temperature_min': round(random.uniform(10, 20), 1),
                'precipitation_totale': round(random.uniform(50, 300), 1),
                'precipitation_moyenne': round(random.uniform(1, 10), 1),
                'tendance_temperature': random.choice(['hausse', 'baisse', 'stable']),
                'tendance_precipitation': random.choice(['hausse', 'baisse', 'stable']),
                'indice_secheresse': round(random.uniform(0, 100), 1)
            }
            
            try:
                tendance_id = models.execute_kw(db, uid, password, 'smart_agri_tendance_climatique', 'create', [tendance_data])
                print(f"  ✅ Tendance {i+1} créée (ID: {tendance_id})")
            except Exception as e:
                print(f"  ❌ Erreur tendance {i+1}: {str(e)[:50]}")
        
        # 5. REMPLIR IMPORTS METEOSTAT (5 enregistrements)
        print("\n📡 AJOUT DE 5 IMPORTS METEOSTAT...")
        print("-" * 40)
        
        stations = [
            {'nom': 'Station Tanger', 'lat': 35.7595, 'lon': -5.8340, 'alt': 20},
            {'nom': 'Station Casablanca', 'lat': 33.5731, 'lon': -7.5898, 'alt': 50},
            {'nom': 'Station Rabat', 'lat': 34.0209, 'lon': -6.8416, 'alt': 75},
            {'nom': 'Station Marrakech', 'lat': 31.6295, 'lon': -7.9811, 'alt': 450},
            {'nom': 'Station Fès', 'lat': 34.0331, 'lon': -5.0003, 'alt': 400}
        ]
        
        for i, station in enumerate(stations):
            meteostat_data = {
                'name': f'Import {station["nom"]} - {datetime.now().strftime("%Y-%m-%d")}',
                'description': f'Import automatique des données Meteostat pour {station["nom"]}',
                'exploitation_id': exploitation_id,
                'station_id': f'STATION_{i+1:03d}',
                'nom_station': station['nom'],
                'latitude': station['lat'],
                'longitude': station['lon'],
                'altitude': station['alt'],
                'scenario_climatique': random.choice(['historique', 'rcp_45', 'rcp_85']),
                'derniere_importation': (datetime.now() - timedelta(hours=random.randint(1, 24))).strftime('%Y-%m-%d %H:%M:%S'),
                'prochaine_import': (datetime.now() + timedelta(hours=random.randint(1, 12))).strftime('%Y-%m-%d %H:%M:%S'),
                'seuil_temperature_max': round(random.uniform(30, 40), 1),
                'seuil_temperature_min': round(random.uniform(-10, 5), 1),
                'seuil_precipitation_min': round(random.uniform(1, 10), 1),
                'seuil_precipitation_max': round(random.uniform(50, 150), 1),
                'seuil_vent_max': round(random.uniform(30, 60), 1)
            }
            
            try:
                meteostat_id = models.execute_kw(db, uid, password, 'smart_agri_meteostat_import', 'create', [meteostat_data])
                print(f"  ✅ Import {station['nom']} créé (ID: {meteostat_id})")
            except Exception as e:
                print(f"  ❌ Erreur import {station['nom']}: {str(e)[:50]}")
        
        # 6. VÉRIFICATION FINALE
        print("\n📊 VÉRIFICATION FINALE - TOUS LES SOUS-MENUS...")
        print("-" * 50)
        
        modeles_climat = [
            'smart_agri_meteo',
            'smart_agri_rcp_scenario',
            'smart_agri_scenario_climatique',
            'smart_agri_alerte_climatique',
            'smart_agri_tendance_climatique',
            'smart_agri_meteostat_import'
        ]
        
        total_records = 0
        for modele in modeles_climat:
            try:
                count = models.execute_kw(db, uid, password, modele, 'search_count', [[]])
                total_records += count
                print(f"  ✅ {modele}: {count} enregistrements")
            except Exception as e:
                print(f"  ❌ {modele}: ERREUR - {str(e)[:50]}")
        
        print(f"\n🎉 TOTAL: {total_records} enregistrements ajoutés!")
        print("🌐 Allez sur http://localhost:10020 pour voir tous les sous-menus remplis!")
        
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")

if __name__ == "__main__":
    fill_all_climate_menus()

