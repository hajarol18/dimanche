#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xmlrpc.client
import random
from datetime import datetime, timedelta

def add_climate_data():
    """Ajouter des données d'exemple dans tous les sous-menus climat"""
    
    # Configuration Odoo
    url = 'http://localhost:10020'
    db = 'odoo123'
    username = 'hajar'
    password = 'hajar'
    
    print("🌤️ AJOUT DE DONNÉES CLIMAT DANS TOUS LES SOUS-MENUS")
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
        
        # 1. AJOUT DE DONNÉES MÉTÉO
        print("\n🌡️ AJOUT DE DONNÉES MÉTÉO...")
        print("-" * 40)
        
        # Récupérer l'exploitation
        exploitation_ids = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'search', [[]])
        exploitation_id = exploitation_ids[0] if exploitation_ids else None
        print(f"✅ Exploitation trouvée: ID {exploitation_id}")
        
        # Ajouter 10 enregistrements météo
        for i in range(10):
            date_mesure = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            meteo_data = {
                'name': f'Mesure météo jour {i+1}',
                'description': f'Données météorologiques du {date_mesure}',
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
                print(f"  ❌ Erreur météo {i+1}: {str(e)[:80]}")
        
        # 2. AJOUT DE SCÉNARIOS RCP
        print("\n🔥 AJOUT DE SCÉNARIOS RCP...")
        print("-" * 40)
        
        rcp_scenarios = [
            {
                'code_rcp': 'rcp_2_6',
                'name': 'RCP 2.6 - Optimiste',
                'description': 'Scénario optimiste avec limitation du réchauffement à +2°C',
                'rechauffement_2030': 1.0,
                'rechauffement_2050': 1.5,
                'rechauffement_2100': 2.0,
                'impact_secheresse': 'faible',
                'impact_precipitation': 'faible',
                'impact_temperature': 'faible'
            },
            {
                'code_rcp': 'rcp_4_5',
                'name': 'RCP 4.5 - Modéré',
                'description': 'Scénario modéré avec réduction des émissions',
                'rechauffement_2030': 1.5,
                'rechauffement_2050': 2.0,
                'rechauffement_2100': 2.4,
                'impact_secheresse': 'modere',
                'impact_precipitation': 'modere',
                'impact_temperature': 'modere'
            },
            {
                'code_rcp': 'rcp_8_5',
                'name': 'RCP 8.5 - Pessimiste',
                'description': 'Scénario pessimiste avec émissions continues élevées',
                'rechauffement_2030': 2.0,
                'rechauffement_2050': 3.0,
                'rechauffement_2100': 4.8,
                'impact_secheresse': 'critique',
                'impact_precipitation': 'eleve',
                'impact_temperature': 'critique'
            }
        ]
        
        for scenario in rcp_scenarios:
            try:
                rcp_id = models.execute_kw(db, uid, password, 'smart_agri_rcp_scenario', 'create', [scenario])
                print(f"  ✅ Scénario RCP créé: {scenario['name']} (ID: {rcp_id})")
            except Exception as e:
                print(f"  ❌ Erreur RCP: {str(e)[:80]}")
        
        # 3. AJOUT D'ALERTES CLIMATIQUES
        print("\n⚠️ AJOUT D'ALERTES CLIMATIQUES...")
        print("-" * 40)
        
        alertes = [
            {
                'name': 'Alerte Sécheresse - Région Tanger',
                'description': 'Période de sécheresse prolongée détectée',
                'exploitation_id': exploitation_id,
                'type_alerte': 'secheresse',
                'niveau': 'orange',
                'date_detection': datetime.now().strftime('%Y-%m-%d'),
                'date_debut': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
                'date_fin': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
                'temperature_actuelle': 32.5,
                'precipitation_7j': 2.1,
                'recommandations': 'Augmenter l\'irrigation, surveiller l\'humidité du sol'
            },
            {
                'name': 'Alerte Canicule - Température élevée',
                'description': 'Température exceptionnellement élevée',
                'exploitation_id': exploitation_id,
                'type_alerte': 'canicule',
                'niveau': 'rouge',
                'date_detection': datetime.now().strftime('%Y-%m-%d'),
                'date_debut': datetime.now().strftime('%Y-%m-%d'),
                'date_fin': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
                'temperature_actuelle': 38.2,
                'recommandations': 'Protéger les cultures sensibles, augmenter l\'irrigation'
            },
            {
                'name': 'Alerte Vent Fort',
                'description': 'Vent fort prévu dans la région',
                'exploitation_id': exploitation_id,
                'type_alerte': 'vent_fort',
                'niveau': 'jaune',
                'date_detection': datetime.now().strftime('%Y-%m-%d'),
                'date_debut': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'date_fin': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
                'vitesse_vent_prevue': 45.0,
                'recommandations': 'Sécuriser les installations, protéger les cultures fragiles'
            }
        ]
        
        for alerte in alertes:
            try:
                alerte_id = models.execute_kw(db, uid, password, 'smart_agri_alerte_climatique', 'create', [alerte])
                print(f"  ✅ Alerte créée: {alerte['name']} (ID: {alerte_id})")
            except Exception as e:
                print(f"  ❌ Erreur alerte: {str(e)[:80]}")
        
        # 4. AJOUT DE TENDANCES CLIMATIQUES
        print("\n📈 AJOUT DE TENDANCES CLIMATIQUES...")
        print("-" * 40)
        
        tendances = [
            {
                'name': 'Tendance Température - 30 jours',
                'description': 'Évolution de la température sur 30 jours',
                'exploitation_id': exploitation_id,
                'periode_debut': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'periode_fin': datetime.now().strftime('%Y-%m-%d'),
                'temperature_moyenne': 25.3,
                'temperature_max': 38.5,
                'temperature_min': 12.1,
                'precipitation_totale': 45.2,
                'tendance_temperature': 'hausse',
                'tendance_precipitation': 'baisse'
            },
            {
                'name': 'Tendance Précipitations - 7 jours',
                'description': 'Évolution des précipitations sur 7 jours',
                'exploitation_id': exploitation_id,
                'periode_debut': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'periode_fin': datetime.now().strftime('%Y-%m-%d'),
                'precipitation_totale': 8.5,
                'precipitation_moyenne': 1.2,
                'tendance_precipitation': 'baisse'
            }
        ]
        
        for tendance in tendances:
            try:
                tendance_id = models.execute_kw(db, uid, password, 'smart_agri_tendance_climatique', 'create', [tendance])
                print(f"  ✅ Tendance créée: {tendance['name']} (ID: {tendance_id})")
            except Exception as e:
                print(f"  ❌ Erreur tendance: {str(e)[:80]}")
        
        # 5. AJOUT D'IMPORT METEOSTAT
        print("\n📡 AJOUT D'IMPORT METEOSTAT...")
        print("-" * 40)
        
        meteostat_data = {
            'name': 'Import Meteostat - Station Tanger',
            'description': 'Import automatique des données Meteostat pour Tanger',
            'exploitation_id': exploitation_id,
            'station_id': 'TANGER_STATION_001',
            'latitude': 35.7595,
            'longitude': -5.8340,
            'altitude': 20,
            'scenario_climatique': 'historique',
            'derniere_importation': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'prochaine_import': (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S'),
            'seuil_temperature_max': 35.0,
            'seuil_temperature_min': -5.0,
            'seuil_precipitation_min': 5.0,
            'seuil_precipitation_max': 100.0,
            'seuil_vent_max': 50.0
        }
        
        try:
            meteostat_id = models.execute_kw(db, uid, password, 'smart_agri_meteostat_import', 'create', [meteostat_data])
            print(f"  ✅ Import Meteostat créé (ID: {meteostat_id})")
        except Exception as e:
            print(f"  ❌ Erreur Meteostat: {str(e)[:80]}")
        
        # 6. VÉRIFICATION FINALE
        print("\n📊 VÉRIFICATION FINALE DES DONNÉES...")
        print("-" * 40)
        
        modeles_climat = [
            'smart_agri_meteo',
            'smart_agri_rcp_scenario',
            'smart_agri_alerte_climatique',
            'smart_agri_tendance_climatique',
            'smart_agri_meteostat_import'
        ]
        
        for modele in modeles_climat:
            try:
                count = models.execute_kw(db, uid, password, modele, 'search_count', [[]])
                print(f"  ✅ {modele}: {count} enregistrements")
            except Exception as e:
                print(f"  ❌ {modele}: ERREUR - {str(e)[:80]}")
        
        print("\n🎉 DONNÉES CLIMAT AJOUTÉES AVEC SUCCÈS!")
        print("🌐 Allez sur http://localhost:10020 pour voir les données")
        
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")

if __name__ == "__main__":
    add_climate_data()
