#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xmlrpc.client
import random
from datetime import datetime, timedelta

def fill_climate_simple():
    """Remplir les sous-menus climat avec des données simples et correctes"""
    
    # Configuration Odoo
    url = 'http://localhost:10020'
    db = 'odoo123'
    username = 'hajar'
    password = 'hajar'
    
    print("🌤️ REMPLISSAGE SIMPLE DES SOUS-MENUS CLIMAT")
    print("=" * 50)
    
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
        
        # 1. AJOUTER DES DONNÉES MÉTÉO SIMPLES
        print("\n🌡️ AJOUT DE DONNÉES MÉTÉO...")
        print("-" * 30)
        
        for i in range(5):
            date_mesure = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            meteo_data = {
                'name': f'Mesure {i+1}',
                'exploitation_id': exploitation_id,
                'date_mesure': date_mesure,
                'temperature': round(random.uniform(20, 30), 1),
                'precipitation': round(random.uniform(0, 20), 1),
                'humidite': round(random.uniform(50, 80), 1)
            }
            
            try:
                meteo_id = models.execute_kw(db, uid, password, 'smart_agri_meteo', 'create', [meteo_data])
                print(f"  ✅ Météo {i+1} créée (ID: {meteo_id})")
            except Exception as e:
                print(f"  ❌ Erreur météo {i+1}: {str(e)[:50]}")
        
        # 2. AJOUTER DES SCÉNARIOS CLIMATIQUES
        print("\n🌍 AJOUT DE SCÉNARIOS CLIMATIQUES...")
        print("-" * 30)
        
        scenarios = [
            {
                'name': 'Scénario Optimiste 2030',
                'code_scenario': 'RCP 2.6',
                'type_scenario': 'rcp26',
                'description': 'Scénario optimiste avec limitation du réchauffement',
                'augmentation_temperature': 1.5,
                'variation_precipitation': 5.0
            },
            {
                'name': 'Scénario Modéré 2050',
                'code_scenario': 'RCP 4.5',
                'type_scenario': 'rcp45',
                'description': 'Scénario modéré avec stabilisation',
                'augmentation_temperature': 2.0,
                'variation_precipitation': -10.0
            },
            {
                'name': 'Scénario Pessimiste 2100',
                'code_scenario': 'RCP 8.5',
                'type_scenario': 'rcp85',
                'description': 'Scénario pessimiste sans action',
                'augmentation_temperature': 4.0,
                'variation_precipitation': -20.0
            }
        ]
        
        for scenario in scenarios:
            try:
                scenario_id = models.execute_kw(db, uid, password, 'smart_agri_scenario_climatique', 'create', [scenario])
                print(f"  ✅ Scénario créé: {scenario['name']} (ID: {scenario_id})")
            except Exception as e:
                print(f"  ❌ Erreur scénario: {str(e)[:50]}")
        
        # 3. AJOUTER DES ALERTES CLIMATIQUES
        print("\n⚠️ AJOUT D'ALERTES CLIMATIQUES...")
        print("-" * 30)
        
        alertes = [
            {
                'name': 'Alerte Sécheresse',
                'exploitation_id': exploitation_id,
                'type_alerte': 'secheresse',
                'niveau': 'orange',
                'description': 'Période de sécheresse détectée'
            },
            {
                'name': 'Alerte Canicule',
                'exploitation_id': exploitation_id,
                'type_alerte': 'canicule',
                'niveau': 'rouge',
                'description': 'Température exceptionnellement élevée'
            },
            {
                'name': 'Alerte Vent Fort',
                'exploitation_id': exploitation_id,
                'type_alerte': 'vent_fort',
                'niveau': 'jaune',
                'description': 'Vent fort prévu'
            }
        ]
        
        for alerte in alertes:
            try:
                alerte_id = models.execute_kw(db, uid, password, 'smart_agri_alerte_climatique', 'create', [alerte])
                print(f"  ✅ Alerte créée: {alerte['name']} (ID: {alerte_id})")
            except Exception as e:
                print(f"  ❌ Erreur alerte: {str(e)[:50]}")
        
        # 4. AJOUTER DES TENDANCES CLIMATIQUES
        print("\n📈 AJOUT DE TENDANCES CLIMATIQUES...")
        print("-" * 30)
        
        tendances = [
            {
                'name': 'Tendance Température 30j',
                'exploitation_id': exploitation_id,
                'periode_debut': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'periode_fin': datetime.now().strftime('%Y-%m-%d'),
                'temperature_moyenne': 25.5,
                'precipitation_totale': 45.2
            },
            {
                'name': 'Tendance Précipitations 7j',
                'exploitation_id': exploitation_id,
                'periode_debut': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'periode_fin': datetime.now().strftime('%Y-%m-%d'),
                'precipitation_totale': 8.5
            }
        ]
        
        for tendance in tendances:
            try:
                tendance_id = models.execute_kw(db, uid, password, 'smart_agri_tendance_climatique', 'create', [tendance])
                print(f"  ✅ Tendance créée: {tendance['name']} (ID: {tendance_id})")
            except Exception as e:
                print(f"  ❌ Erreur tendance: {str(e)[:50]}")
        
        # 5. VÉRIFICATION FINALE
        print("\n📊 VÉRIFICATION FINALE...")
        print("-" * 30)
        
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
        
        print(f"\n🎉 TOTAL: {total_records} enregistrements!")
        print("🌐 Allez sur http://localhost:10020 pour voir les sous-menus remplis!")
        
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")

if __name__ == "__main__":
    fill_climate_simple()

