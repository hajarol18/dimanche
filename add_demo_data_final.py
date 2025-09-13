#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT FINAL POUR AJOUTER DES DONNÉES DE DÉMONSTRATION
Utilise les bons noms de champs pour éviter les erreurs
"""

import xmlrpc.client
from datetime import datetime, timedelta
import random

def add_demo_data_final():
    """Ajoute des données de démonstration avec les bons noms de champs"""
    
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        print("🌾 AJOUT DE DONNÉES DE DÉMONSTRATION FINALES")
        print("=" * 50)
        
        # Connexion
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        print("✅ Connecté à Odoo")
        
        # 1. Créer des types de sol avec le champ code
        print("\n🌱 Création des types de sol...")
        soil_types = [
            {'name': 'Sol Argileux', 'code': 'ARG', 'description': 'Sol riche en argile, bon pour les céréales'},
            {'name': 'Sol Sableux', 'code': 'SAB', 'description': 'Sol drainant, idéal pour les légumes'},
            {'name': 'Sol Limoneux', 'code': 'LIM', 'description': 'Sol équilibré, polyvalent'},
        ]
        
        for soil in soil_types:
            try:
                soil_id = models.execute_kw(db, uid, password, 'smart_agri_soil_type', 'create', [soil])
                print(f"  ✅ {soil['name']} (ID: {soil_id})")
            except Exception as e:
                print(f"  ⚠️ Erreur {soil['name']}: {str(e)}")
        
        # 2. Créer des parcelles avec les bons noms de champs
        print("\n🗺️ Création des parcelles...")
        parcelles = [
            {
                'name': 'Parcelle A1 - Blé Dur',
                'exploitation_id': 1,
                'surface': 5.2,
                'texture': 'argileuse',
                'ph': 6.8,
                'irrigation': True,
                'type_irrigation': 'aspersion'
            },
            {
                'name': 'Parcelle A2 - Orge',
                'exploitation_id': 1,
                'surface': 3.8,
                'texture': 'argileuse',
                'ph': 6.5,
                'irrigation': True,
                'type_irrigation': 'gravitaire'
            },
            {
                'name': 'Parcelle B1 - Tomates',
                'exploitation_id': 2,
                'surface': 2.5,
                'texture': 'sableuse',
                'ph': 6.2,
                'irrigation': True,
                'type_irrigation': 'goutte_a_goutte'
            }
        ]
        
        for parc in parcelles:
            try:
                parc_id = models.execute_kw(db, uid, password, 'smart_agri_parcelle', 'create', [parc])
                print(f"  ✅ {parc['name']} (ID: {parc_id})")
            except Exception as e:
                print(f"  ⚠️ Erreur {parc['name']}: {str(e)}")
        
        # 3. Créer des cultures avec les bons noms de champs
        print("\n🌾 Création des cultures...")
        cultures = [
            {
                'name': 'Blé Dur Hiver',
                'type_culture': 'cereales',
                'famille': 'cereales',
                'duree_cycle': 180,
                'date_semis': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=150)).strftime('%Y-%m-%d'),
                'exploitation_id': 1
            },
            {
                'name': 'Orge Fourragère',
                'type_culture': 'cereales',
                'famille': 'cereales',
                'duree_cycle': 160,
                'date_semis': (datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=135)).strftime('%Y-%m-%d'),
                'exploitation_id': 1
            },
            {
                'name': 'Tomates Cerises',
                'type_culture': 'legumes',
                'famille': 'legumes',
                'duree_cycle': 120,
                'date_semis': (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=105)).strftime('%Y-%m-%d'),
                'exploitation_id': 2
            }
        ]
        
        for cult in cultures:
            try:
                cult_id = models.execute_kw(db, uid, password, 'smart_agri_culture', 'create', [cult])
                print(f"  ✅ {cult['name']} (ID: {cult_id})")
            except Exception as e:
                print(f"  ⚠️ Erreur {cult['name']}: {str(e)}")
        
        # 4. Créer des données météo avec les bons noms de champs
        print("\n🌤️ Création des données météo...")
        for i in range(7):  # 7 jours de données
            date_meteo = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            meteo_data = {
                'date_meteo': date_meteo,
                'temperature_moyenne': round(20 + random.uniform(-5, 10), 1),
                'precipitation': round(random.uniform(0, 15), 1),
                'humidite_relative': round(60 + random.uniform(-20, 20), 1),
                'station': 'Station Météo Casablanca'
            }
            
            try:
                meteo_id = models.execute_kw(db, uid, password, 'smart_agri_meteo', 'create', [meteo_data])
                if i % 3 == 0:
                    print(f"  ✅ Données météo pour {date_meteo}")
            except Exception as e:
                print(f"  ⚠️ Erreur météo {date_meteo}: {str(e)}")
        
        print("\n🎉 DONNÉES DE DÉMONSTRATION AJOUTÉES !")
        print("🌐 Allez sur http://localhost:10020 pour voir les données")
        print("📊 Vos menus sont maintenant remplis de données réalistes")
        print("🎯 Prêt pour votre soutenance !")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

if __name__ == "__main__":
    add_demo_data_final()
