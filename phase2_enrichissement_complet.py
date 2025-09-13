#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PHASE 2: ENRICHISSEMENT COMPLET DU MODULE
Création de données réalistes et complètes pour un travail de 3 mois
"""

import xmlrpc.client
from datetime import datetime, timedelta
import random

def phase2_enrichissement_complet():
    """Phase 2: Enrichissement complet avec données réalistes"""
    
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        print("🚀 PHASE 2: ENRICHISSEMENT COMPLET DU MODULE")
        print("=" * 70)
        print("🎯 Création de données réalistes pour un travail de 3 mois")
        print("=" * 70)
        
        # Connexion
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        print("✅ Connecté à Odoo")
        
        # 1. CRÉER DES EXPLOITATIONS AGRICOLES MAROCAINES RÉALISTES
        print("\n🏡 CRÉATION D'EXPLOITATIONS AGRICOLES MAROCAINES")
        print("-" * 60)
        
        exploitations_maroc = [
            {
                'name': 'Domaine Agricole de la Chaouia',
                'code': 'CHA001',
                'description': 'Exploitation familiale spécialisée dans les céréales et l\'élevage',
                'superficie_totale': 45.5,
                'proprietaire': 'Famille El Fassi',
                'telephone': '+212 5 22 12 34 56',
                'email': 'contact@domaine-chaouia.ma',
                'latitude': 33.5731,
                'longitude': -7.5898,
                'state': 'actif'
            },
            {
                'name': 'Coopérative Agricole du Souss',
                'code': 'SOU002',
                'description': 'Coopérative moderne spécialisée dans l\'agrumiculture et l\'avocat',
                'superficie_totale': 120.0,
                'proprietaire': 'Coopérative Souss Massa',
                'telephone': '+212 5 28 98 76 54',
                'email': 'info@coop-souss.ma',
                'latitude': 30.4278,
                'longitude': -9.5981,
                'state': 'actif'
            },
            {
                'name': 'Ferme High-Tech de Meknès',
                'code': 'MEK003',
                'description': 'Ferme technologique avec serres intelligentes et IoT',
                'superficie_totale': 25.0,
                'proprietaire': 'AgriTech Solutions',
                'telephone': '+212 5 35 55 12 34',
                'email': 'contact@agritech-meknes.ma',
                'latitude': 33.8935,
                'longitude': -5.5473,
                'state': 'actif'
            },
            {
                'name': 'Domaine Viticole de Fès',
                'code': 'FES004',
                'description': 'Domaine viticole de prestige produisant des vins d\'appellation',
                'superficie_totale': 35.0,
                'proprietaire': 'Famille Benjelloun',
                'telephone': '+212 5 35 66 77 88',
                'email': 'vins@domaine-fes.ma',
                'latitude': 34.0331,
                'longitude': -5.0003,
                'state': 'actif'
            },
            {
                'name': 'Exploitation Oléicole de Marrakech',
                'code': 'MAR005',
                'description': 'Exploitation traditionnelle d\'oliviers avec huilerie moderne',
                'superficie_totale': 80.0,
                'proprietaire': 'Famille Alaoui',
                'telephone': '+212 5 24 44 55 66',
                'email': 'huile@olive-marrakech.ma',
                'latitude': 31.6295,
                'longitude': -7.9811,
                'state': 'actif'
            }
        ]
        
        exploitation_ids = []
        for exp in exploitations_maroc:
            try:
                exp_id = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'create', [exp])
                exploitation_ids.append(exp_id)
                print(f"  ✅ {exp['name']} (ID: {exp_id}) - {exp['superficie_totale']} ha")
            except Exception as e:
                print(f"  ❌ Erreur {exp['name']}: {str(e)}")
        
        # 2. CRÉER DES PARCELLES DÉTAILLÉES POUR CHAQUE EXPLOITATION
        print("\n🗺️ CRÉATION DE PARCELLES DÉTAILLÉES")
        print("-" * 60)
        
        parcelles_detaillees = [
            # Domaine de la Chaouia - Céréales
            {
                'name': 'Parcelle Céréales A1 - Blé Dur',
                'exploitation_id': exploitation_ids[0] if exploitation_ids else 1,
                'surface': 12.5,
                'texture': 'argileuse',
                'ph': 6.8,
                'altitude': 450,
                'irrigation': True,
                'type_irrigation': 'aspersion',
                'drainage': True,
                'forme': 'rectangulaire',
                'source_geo_data': 'gps',
                'precision_geo': 2.0,
                'description': 'Parcelle principale pour la culture du blé dur d\'hiver'
            },
            {
                'name': 'Parcelle Céréales A2 - Orge',
                'exploitation_id': exploitation_ids[0] if exploitation_ids else 1,
                'surface': 8.0,
                'texture': 'argileuse',
                'ph': 6.5,
                'altitude': 445,
                'irrigation': True,
                'type_irrigation': 'gravitaire',
                'drainage': True,
                'forme': 'rectangulaire',
                'source_geo_data': 'gps',
                'precision_geo': 2.0,
                'description': 'Parcelle pour l\'orge fourragère'
            },
            {
                'name': 'Parcelle Élevage A3 - Pâturage',
                'exploitation_id': exploitation_ids[0] if exploitation_ids else 1,
                'surface': 15.0,
                'texture': 'limoneuse',
                'ph': 6.7,
                'altitude': 455,
                'irrigation': False,
                'drainage': True,
                'forme': 'irreguliere',
                'source_geo_data': 'manual',
                'precision_geo': 5.0,
                'description': 'Pâturage pour l\'élevage bovin'
            },
            # Coopérative du Souss - Agrumes
            {
                'name': 'Verger Agrumes B1 - Oranges Navel',
                'exploitation_id': exploitation_ids[1] if len(exploitation_ids) > 1 else 1,
                'surface': 25.0,
                'texture': 'sableuse',
                'ph': 6.2,
                'altitude': 300,
                'irrigation': True,
                'type_irrigation': 'goutte_a_goutte',
                'drainage': True,
                'forme': 'rectangulaire',
                'source_geo_data': 'gps',
                'precision_geo': 1.0,
                'description': 'Verger d\'oranges Navel de qualité export'
            },
            {
                'name': 'Verger Agrumes B2 - Mandarines',
                'exploitation_id': exploitation_ids[1] if len(exploitation_ids) > 1 else 1,
                'surface': 20.0,
                'texture': 'sableuse',
                'ph': 6.0,
                'altitude': 305,
                'irrigation': True,
                'type_irrigation': 'goutte_a_goutte',
                'drainage': True,
                'forme': 'rectangulaire',
                'source_geo_data': 'gps',
                'precision_geo': 1.0,
                'description': 'Verger de mandarines Clementine'
            },
            {
                'name': 'Parcelle Avocatiers B3',
                'exploitation_id': exploitation_ids[1] if len(exploitation_ids) > 1 else 1,
                'surface': 15.0,
                'texture': 'limoneuse',
                'ph': 6.5,
                'altitude': 310,
                'irrigation': True,
                'type_irrigation': 'goutte_a_goutte',
                'drainage': True,
                'forme': 'rectangulaire',
                'source_geo_data': 'gps',
                'precision_geo': 1.5,
                'description': 'Parcelle d\'avocatiers Hass'
            },
            # Ferme High-Tech de Meknès - Serres
            {
                'name': 'Serre High-Tech C1 - Tomates',
                'exploitation_id': exploitation_ids[2] if len(exploitation_ids) > 2 else 1,
                'surface': 2.5,
                'texture': 'sableuse',
                'ph': 6.2,
                'altitude': 200,
                'irrigation': True,
                'type_irrigation': 'goutte_a_goutte',
                'drainage': True,
                'forme': 'rectangulaire',
                'source_geo_data': 'gps',
                'precision_geo': 0.5,
                'description': 'Serre intelligente avec capteurs IoT'
            },
            {
                'name': 'Serre High-Tech C2 - Concombres',
                'exploitation_id': exploitation_ids[2] if len(exploitation_ids) > 2 else 1,
                'surface': 2.0,
                'texture': 'sableuse',
                'ph': 6.0,
                'altitude': 200,
                'irrigation': True,
                'type_irrigation': 'goutte_a_goutte',
                'drainage': True,
                'forme': 'rectangulaire',
                'source_geo_data': 'gps',
                'precision_geo': 0.5,
                'description': 'Serre avec système de refroidissement'
            },
            # Domaine Viticole de Fès
            {
                'name': 'Vignoble Syrah D1',
                'exploitation_id': exploitation_ids[3] if len(exploitation_ids) > 3 else 1,
                'surface': 12.0,
                'texture': 'calcaire',
                'ph': 7.1,
                'altitude': 600,
                'irrigation': False,
                'drainage': True,
                'forme': 'rectangulaire',
                'source_geo_data': 'gps',
                'precision_geo': 1.0,
                'description': 'Vignoble de Syrah pour vins rouges'
            },
            {
                'name': 'Vignoble Chardonnay D2',
                'exploitation_id': exploitation_ids[3] if len(exploitation_ids) > 3 else 1,
                'surface': 8.0,
                'texture': 'calcaire',
                'ph': 7.0,
                'altitude': 610,
                'irrigation': False,
                'drainage': True,
                'forme': 'rectangulaire',
                'source_geo_data': 'gps',
                'precision_geo': 1.0,
                'description': 'Vignoble de Chardonnay pour vins blancs'
            },
            # Exploitation Oléicole de Marrakech
            {
                'name': 'Verger Oliviers E1 - Picholine',
                'exploitation_id': exploitation_ids[4] if len(exploitation_ids) > 4 else 1,
                'surface': 30.0,
                'texture': 'argileuse',
                'ph': 7.2,
                'altitude': 400,
                'irrigation': True,
                'type_irrigation': 'goutte_a_goutte',
                'drainage': True,
                'forme': 'irreguliere',
                'source_geo_data': 'gps',
                'precision_geo': 3.0,
                'description': 'Verger d\'oliviers Picholine du Maroc'
            },
            {
                'name': 'Verger Oliviers E2 - Arbequina',
                'exploitation_id': exploitation_ids[4] if len(exploitation_ids) > 4 else 1,
                'surface': 25.0,
                'texture': 'limoneuse',
                'ph': 6.8,
                'altitude': 395,
                'irrigation': True,
                'type_irrigation': 'goutte_a_goutte',
                'drainage': True,
                'forme': 'irreguliere',
                'source_geo_data': 'gps',
                'precision_geo': 3.0,
                'description': 'Verger d\'oliviers Arbequina'
            }
        ]
        
        parcelle_ids = []
        for parc in parcelles_detaillees:
            try:
                parc_id = models.execute_kw(db, uid, password, 'smart_agri_parcelle', 'create', [parc])
                parcelle_ids.append(parc_id)
                print(f"  ✅ {parc['name']} (ID: {parc_id}) - {parc['surface']} ha")
            except Exception as e:
                print(f"  ❌ Erreur {parc['name']}: {str(e)}")
        
        # 3. CRÉER DES CULTURES RÉALISTES
        print("\n🌾 CRÉATION DE CULTURES RÉALISTES")
        print("-" * 60)
        
        cultures_realistes = [
            # Céréales - Domaine de la Chaouia
            {
                'name': 'Blé Dur Hiver - Variété Karim',
                'type_culture': 'cereales',
                'famille': 'cereales',
                'duree_cycle': 180,
                'surface_utilisee': 12.5,
                'date_plantation': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=150)).strftime('%Y-%m-%d'),
                'exploitation_id': exploitation_ids[0] if exploitation_ids else 1,
                'parcelle_id': parcelle_ids[0] if parcelle_ids else 1,
                'state': 'active',
                'rendement_moyen': 4.5
            },
            {
                'name': 'Orge Fourragère - Variété Amira',
                'type_culture': 'cereales',
                'famille': 'cereales',
                'duree_cycle': 160,
                'surface_utilisee': 8.0,
                'date_plantation': (datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=135)).strftime('%Y-%m-%d'),
                'exploitation_id': exploitation_ids[0] if exploitation_ids else 1,
                'parcelle_id': parcelle_ids[1] if len(parcelle_ids) > 1 else 1,
                'state': 'active',
                'rendement_moyen': 3.8
            },
            # Agrumes - Coopérative du Souss
            {
                'name': 'Oranges Navel - Variété Washington',
                'type_culture': 'fruits',
                'famille': 'fruits',
                'duree_cycle': 365,
                'surface_utilisee': 25.0,
                'date_plantation': (datetime.now() - timedelta(days=365*3)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
                'exploitation_id': exploitation_ids[1] if len(exploitation_ids) > 1 else 1,
                'parcelle_id': parcelle_ids[3] if len(parcelle_ids) > 3 else 1,
                'state': 'active',
                'rendement_moyen': 35.0
            },
            {
                'name': 'Mandarines Clementine',
                'type_culture': 'fruits',
                'famille': 'fruits',
                'duree_cycle': 365,
                'surface_utilisee': 20.0,
                'date_plantation': (datetime.now() - timedelta(days=365*2)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
                'exploitation_id': exploitation_ids[1] if len(exploitation_ids) > 1 else 1,
                'parcelle_id': parcelle_ids[4] if len(parcelle_ids) > 4 else 1,
                'state': 'active',
                'rendement_moyen': 28.0
            },
            # Serres - Ferme High-Tech
            {
                'name': 'Tomates Cerises - Variété Cherry',
                'type_culture': 'legumes',
                'famille': 'legumes',
                'duree_cycle': 120,
                'surface_utilisee': 2.5,
                'date_plantation': (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=105)).strftime('%Y-%m-%d'),
                'exploitation_id': exploitation_ids[2] if len(exploitation_ids) > 2 else 1,
                'parcelle_id': parcelle_ids[6] if len(parcelle_ids) > 6 else 1,
                'state': 'active',
                'rendement_moyen': 45.0
            },
            # Vigne - Domaine de Fès
            {
                'name': 'Vigne Syrah - Cépage Premium',
                'type_culture': 'viticulture',
                'famille': 'viticulture',
                'duree_cycle': 365,
                'surface_utilisee': 12.0,
                'date_plantation': (datetime.now() - timedelta(days=365*4)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'exploitation_id': exploitation_ids[3] if len(exploitation_ids) > 3 else 1,
                'parcelle_id': parcelle_ids[8] if len(parcelle_ids) > 8 else 1,
                'state': 'active',
                'rendement_moyen': 8.5
            },
            # Oliviers - Marrakech
            {
                'name': 'Oliviers Picholine - Variété Marocaine',
                'type_culture': 'arboriculture',
                'famille': 'arboriculture',
                'duree_cycle': 365,
                'surface_utilisee': 30.0,
                'date_plantation': (datetime.now() - timedelta(days=365*5)).strftime('%Y-%m-%d'),
                'date_recolte_prevue': (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'),
                'exploitation_id': exploitation_ids[4] if len(exploitation_ids) > 4 else 1,
                'parcelle_id': parcelle_ids[10] if len(parcelle_ids) > 10 else 1,
                'state': 'active',
                'rendement_moyen': 12.0
            }
        ]
        
        culture_ids = []
        for cult in cultures_realistes:
            try:
                cult_id = models.execute_kw(db, uid, password, 'smart_agri_culture', 'create', [cult])
                culture_ids.append(cult_id)
                print(f"  ✅ {cult['name']} (ID: {cult_id}) - {cult['surface_utilisee']} ha")
            except Exception as e:
                print(f"  ❌ Erreur {cult['name']}: {str(e)}")
        
        # 4. CRÉER DES DONNÉES MÉTÉO HISTORIQUES
        print("\n🌤️ CRÉATION DE DONNÉES MÉTÉO HISTORIQUES")
        print("-" * 60)
        
        # Créer 90 jours de données météo (3 mois)
        for i in range(90):
            date_meteo = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            # Données météo réalistes pour le Maroc
            temperature_base = 22 + random.uniform(-8, 12)  # 14-34°C
            precipitation = random.uniform(0, 25) if random.random() < 0.3 else 0  # 30% de chance de pluie
            humidite = 60 + random.uniform(-25, 25)  # 35-85%
            
            meteo_data = {
                'date': date_meteo,
                'temperature_moyenne': round(temperature_base, 1),
                'precipitation': round(precipitation, 1),
                'humidite_relative': round(humidite, 1),
                'station': 'Station Météo Casablanca'
            }
            
            try:
                meteo_id = models.execute_kw(db, uid, password, 'smart_agri_meteo', 'create', [meteo_data])
                if i % 10 == 0:
                    print(f"  ✅ Données météo pour {date_meteo} - Temp: {meteo_data['temperature_moyenne']}°C")
            except Exception as e:
                print(f"  ❌ Erreur météo {date_meteo}: {str(e)}")
        
        # 5. RÉSUMÉ FINAL DE LA PHASE 2
        print("\n🎉 RÉSUMÉ DE LA PHASE 2")
        print("=" * 60)
        
        # Compter les données créées
        total_exploitations = len(models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'search_count', [[]]))
        total_parcelles = len(models.execute_kw(db, uid, password, 'smart_agri_parcelle', 'search_count', [[]]))
        total_cultures = len(models.execute_kw(db, uid, password, 'smart_agri_culture', 'search_count', [[]]))
        total_meteo = len(models.execute_kw(db, uid, password, 'smart_agri_meteo', 'search_count', [[]]))
        
        print(f"✅ Exploitations agricoles marocaines: {total_exploitations}")
        print(f"✅ Parcelles détaillées: {total_parcelles}")
        print(f"✅ Cultures réalistes: {total_cultures}")
        print(f"✅ Données météo historiques: {total_meteo}")
        print(f"📊 Total: {total_exploitations + total_parcelles + total_cultures + total_meteo} enregistrements")
        
        print(f"\n🎯 VOTRE MODULE EST MAINTENANT EXCEPTIONNEL !")
        print(f"📋 Données réalistes et complètes pour la soutenance")
        print(f"🏡 Exploitations agricoles marocaines authentiques")
        print(f"🌾 Cultures variées et spécialisées")
        print(f"🌤️ Données météo historiques sur 3 mois")
        print(f"🚀 Prêt pour la Phase 3: Intelligence Artificielle")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la Phase 2: {str(e)}")
        return False

if __name__ == "__main__":
    phase2_enrichissement_complet()
