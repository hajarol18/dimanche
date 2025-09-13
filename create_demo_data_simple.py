#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT SIMPLE POUR CRÉER DES DONNÉES DE DÉMONSTRATION
Crée des données de base pour la soutenance
"""

import xmlrpc.client
from datetime import datetime, timedelta
import random

def create_demo_data():
    """Crée des données de démonstration simples"""
    
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        print("🌾 CRÉATION DES DONNÉES DE DÉMONSTRATION")
        print("=" * 50)
        
        # Connexion
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        print("✅ Connecté à Odoo")
        
        # 1. Créer des types de sol
        print("\n🌱 Création des types de sol...")
        soil_types = [
            {'name': 'Sol Argileux', 'description': 'Sol riche en argile, bon pour les céréales'},
            {'name': 'Sol Sableux', 'description': 'Sol drainant, idéal pour les légumes'},
            {'name': 'Sol Limoneux', 'description': 'Sol équilibré, polyvalent'},
        ]
        
        for soil in soil_types:
            try:
                soil_id = models.execute_kw(db, uid, password, 'smart_agri_soil_type', 'create', [soil])
                print(f"  ✅ {soil['name']} (ID: {soil_id})")
            except Exception as e:
                print(f"  ⚠️ Erreur {soil['name']}: {str(e)}")
        
        # 2. Créer des exploitations
        print("\n🏡 Création des exploitations...")
        exploitations = [
            {
                'name': 'Exploitation Familiale Benali',
                'proprietaire': 'Ahmed Benali',
                'telephone': '+212 6 12 34 56 78',
                'superficie_totale': 25.5,
                'state': 'actif'
            },
            {
                'name': 'Coopérative Agricole Al-Maghrib',
                'proprietaire': 'Coopérative Al-Maghrib',
                'telephone': '+212 5 24 12 34 56',
                'superficie_totale': 150.0,
                'state': 'actif'
            }
        ]
        
        exploitation_ids = []
        for exp in exploitations:
            try:
                exp_id = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'create', [exp])
                exploitation_ids.append(exp_id)
                print(f"  ✅ {exp['name']} (ID: {exp_id})")
            except Exception as e:
                print(f"  ⚠️ Erreur {exp['name']}: {str(e)}")
        
        # 3. Créer des parcelles
        print("\n🗺️ Création des parcelles...")
        parcelles = [
            {
                'name': 'Parcelle A1 - Blé Dur',
                'exploitation_id': exploitation_ids[0] if exploitation_ids else 1,
                'surface': 5.2,
                'type_sol': 'argileux'
            },
            {
                'name': 'Parcelle A2 - Orge',
                'exploitation_id': exploitation_ids[0] if exploitation_ids else 1,
                'surface': 3.8,
                'type_sol': 'argileux'
            },
            {
                'name': 'Parcelle B1 - Tomates',
                'exploitation_id': exploitation_ids[1] if len(exploitation_ids) > 1 else 1,
                'surface': 2.5,
                'type_sol': 'sableux'
            }
        ]
        
        for parc in parcelles:
            try:
                parc_id = models.execute_kw(db, uid, password, 'smart_agri_parcelle', 'create', [parc])
                print(f"  ✅ {parc['name']} (ID: {parc_id})")
            except Exception as e:
                print(f"  ⚠️ Erreur {parc['name']}: {str(e)}")
        
        # 4. Créer des cultures
        print("\n🌾 Création des cultures...")
        cultures = [
            {
                'name': 'Blé Dur Hiver',
                'type_culture': 'cereales',
                'variete': 'Karim',
                'date_semis': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=150)).strftime('%Y-%m-%d')
            },
            {
                'name': 'Orge Fourragère',
                'type_culture': 'cereales',
                'variete': 'Amira',
                'date_semis': (datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=135)).strftime('%Y-%m-%d')
            },
            {
                'name': 'Tomates Cerises',
                'type_culture': 'legumes',
                'variete': 'Cherry Red',
                'date_semis': (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=105)).strftime('%Y-%m-%d')
            }
        ]
        
        for cult in cultures:
            try:
                cult_id = models.execute_kw(db, uid, password, 'smart_agri_culture', 'create', [cult])
                print(f"  ✅ {cult['name']} (ID: {cult_id})")
            except Exception as e:
                print(f"  ⚠️ Erreur {cult['name']}: {str(e)}")
        
        # 5. Créer des données météo
        print("\n🌤️ Création des données météo...")
        for i in range(10):  # 10 jours de données
            date_meteo = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            meteo_data = {
                'date': date_meteo,
                'temperature_moyenne': round(20 + random.uniform(-5, 10), 1),
                'precipitation': round(random.uniform(0, 15), 1),
                'humidite_relative': round(60 + random.uniform(-20, 20), 1),
                'station': 'Station Météo Casablanca'
            }
            
            try:
                meteo_id = models.execute_kw(db, uid, password, 'smart_agri_meteo', 'create', [meteo_data])
                if i % 5 == 0:
                    print(f"  ✅ Données météo pour {date_meteo}")
            except Exception as e:
                print(f"  ⚠️ Erreur météo {date_meteo}: {str(e)}")
        
        print("\n🎉 DONNÉES DE DÉMONSTRATION CRÉÉES !")
        print("🌐 Allez sur http://localhost:10020 pour voir les données")
        print("📊 Vos menus sont maintenant remplis de données réalistes")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

if __name__ == "__main__":
    create_demo_data()
