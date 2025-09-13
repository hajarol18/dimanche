#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xmlrpc.client
import random
from datetime import datetime, timedelta

def fill_remaining_data():
    """Remplir les sous-menus restants avec plus de données"""
    
    # Configuration Odoo
    url = 'http://localhost:10020'
    db = 'odoo123'
    username = 'hajar'
    password = 'hajar'
    
    print("🌤️ REMPLISSAGE DES DONNÉES RESTANTES")
    print("=" * 40)
    
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
        
        # 1. AJOUTER PLUS DE DONNÉES MÉTÉO
        print("\n🌡️ AJOUT DE PLUS DE DONNÉES MÉTÉO...")
        print("-" * 35)
        
        for i in range(10):
            date_mesure = (datetime.now() - timedelta(days=i+5)).strftime('%Y-%m-%d')
            
            meteo_data = {
                'name': f'Mesure météo {i+6}',
                'exploitation_id': exploitation_id,
                'date_mesure': date_mesure,
                'temperature': round(random.uniform(18, 32), 1),
                'precipitation': round(random.uniform(0, 25), 1),
                'humidite': round(random.uniform(45, 85), 1),
                'vitesse_vent': round(random.uniform(5, 20), 1)
            }
            
            try:
                meteo_id = models.execute_kw(db, uid, password, 'smart_agri_meteo', 'create', [meteo_data])
                print(f"  ✅ Météo {i+6} créée (ID: {meteo_id})")
            except Exception as e:
                print(f"  ❌ Erreur météo {i+6}: {str(e)[:50]}")
        
        # 2. AJOUTER PLUS D'ALERTES CLIMATIQUES
        print("\n⚠️ AJOUT DE PLUS D'ALERTES...")
        print("-" * 35)
        
        types_alertes = ['gel', 'inondation', 'grele', 'humidite_faible']
        niveaux = ['jaune', 'orange', 'rouge']
        
        for i in range(7):
            alerte_data = {
                'name': f'Alerte {types_alertes[i % len(types_alertes)].title()} {i+1}',
                'exploitation_id': exploitation_id,
                'type_alerte': types_alertes[i % len(types_alertes)],
                'niveau': niveaux[i % len(niveaux)],
                'description': f'Description de l\'alerte {i+1}',
                'date_detection': (datetime.now() - timedelta(days=random.randint(0, 10))).strftime('%Y-%m-%d')
            }
            
            try:
                alerte_id = models.execute_kw(db, uid, password, 'smart_agri_alerte_climatique', 'create', [alerte_data])
                print(f"  ✅ Alerte {i+1} créée (ID: {alerte_id})")
            except Exception as e:
                print(f"  ❌ Erreur alerte {i+1}: {str(e)[:50]}")
        
        # 3. AJOUTER PLUS DE TENDANCES CLIMATIQUES
        print("\n📈 AJOUT DE PLUS DE TENDANCES...")
        print("-" * 35)
        
        for i in range(5):
            periode_debut = (datetime.now() - timedelta(days=15*i)).strftime('%Y-%m-%d')
            periode_fin = (datetime.now() - timedelta(days=15*i-15)).strftime('%Y-%m-%d')
            
            tendance_data = {
                'name': f'Tendance Période {i+1}',
                'exploitation_id': exploitation_id,
                'periode_debut': periode_debut,
                'periode_fin': periode_fin,
                'temperature_moyenne': round(random.uniform(20, 28), 1),
                'precipitation_totale': round(random.uniform(20, 80), 1),
                'tendance_temperature': random.choice(['hausse', 'baisse', 'stable']),
                'tendance_precipitation': random.choice(['hausse', 'baisse', 'stable'])
            }
            
            try:
                tendance_id = models.execute_kw(db, uid, password, 'smart_agri_tendance_climatique', 'create', [tendance_data])
                print(f"  ✅ Tendance {i+1} créée (ID: {tendance_id})")
            except Exception as e:
                print(f"  ❌ Erreur tendance {i+1}: {str(e)[:50]}")
        
        # 4. AJOUTER PLUS D'IMPORTS METEOSTAT
        print("\n📡 AJOUT DE PLUS D'IMPORTS METEOSTAT...")
        print("-" * 35)
        
        stations = [
            {'nom': 'Station Agadir', 'lat': 30.4278, 'lon': -9.5981, 'alt': 25},
            {'nom': 'Station Meknès', 'lat': 33.8935, 'lon': -5.5473, 'alt': 500},
            {'nom': 'Station Oujda', 'lat': 34.6814, 'lon': -1.9086, 'alt': 470}
        ]
        
        for i, station in enumerate(stations):
            meteostat_data = {
                'name': f'Import {station["nom"]}',
                'exploitation_id': exploitation_id,
                'station_id': f'STATION_{i+6:03d}',
                'nom_station': station['nom'],
                'latitude': station['lat'],
                'longitude': station['lon'],
                'altitude': station['alt'],
                'scenario_climatique': random.choice(['historique', 'rcp_45', 'rcp_85']),
                'derniere_importation': (datetime.now() - timedelta(hours=random.randint(1, 48))).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            try:
                meteostat_id = models.execute_kw(db, uid, password, 'smart_agri_meteostat_import', 'create', [meteostat_data])
                print(f"  ✅ Import {station['nom']} créé (ID: {meteostat_id})")
            except Exception as e:
                print(f"  ❌ Erreur import {station['nom']}: {str(e)[:50]}")
        
        # 5. VÉRIFICATION FINALE
        print("\n📊 VÉRIFICATION FINALE COMPLÈTE...")
        print("-" * 40)
        
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
                status = "✅" if count > 0 else "⚠️"
                print(f"  {status} {modele}: {count} enregistrements")
            except Exception as e:
                print(f"  ❌ {modele}: ERREUR - {str(e)[:50]}")
        
        print(f"\n🎉 TOTAL FINAL: {total_records} enregistrements!")
        print("🌐 Tous les sous-menus climat sont maintenant remplis!")
        print("🔗 Allez sur http://localhost:10020 pour voir les résultats!")
        
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")

if __name__ == "__main__":
    fill_remaining_data()

