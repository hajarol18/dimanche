#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUIDE D'UTILISATION - IMPORT METEOSTAT
Comment utiliser la nouvelle fonctionnalité Meteostat
"""

import xmlrpc.client
from datetime import datetime, timedelta

def guide_import_meteostat():
    """Guide complet pour utiliser l'import Meteostat"""
    
    print("📡 GUIDE D'UTILISATION - IMPORT METEOSTAT")
    print("=" * 50)
    
    # Configuration de connexion
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        # Connexion à Odoo
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if not uid:
            print("❌ Échec de l'authentification")
            return False
        
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        print("✅ Connexion réussie à Odoo")
        
        # ÉTAPE 1: Vérifier qu'il y a des exploitations
        print("\n🏭 ÉTAPE 1: Vérifier les exploitations...")
        exploitations = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'search_read', 
                                        [[]], {'fields': ['id', 'name', 'latitude', 'longitude']})
        
        if not exploitations:
            print("❌ Aucune exploitation trouvée. Créons-en une...")
            
            # Créer une exploitation de test
            exploitation_data = {
                'name': 'Exploitation Test - Meteostat',
                'region': 'Casablanca-Settat',
                'surface_totale': 100.0,
                'latitude': 33.5731,  # Casablanca
                'longitude': -7.5898,
                'type_exploitation': 'mixte'
            }
            
            exploitation_id = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'create', [exploitation_data])
            print(f"✅ Exploitation créée (ID: {exploitation_id})")
        else:
            exploitation_id = exploitations[0]['id']
            print(f"✅ Exploitation trouvée: {exploitations[0]['name']} (ID: {exploitation_id})")
        
        # ÉTAPE 2: Créer un import Meteostat
        print("\n📡 ÉTAPE 2: Créer un import Meteostat...")
        
        import_data = {
            'name': 'Import Meteostat - Casablanca - Test',
            'exploitation_id': exploitation_id,
            'station_id': 'CASA001',  # Station Casablanca
            'latitude': 33.5731,      # Casablanca
            'longitude': -7.5898,
            'date_debut': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'date_fin': datetime.now().strftime('%Y-%m-%d'),
            'api_key': 'demo_key'  # Clé de démonstration
        }
        
        import_id = models.execute_kw(db, uid, password, 'smart_agri_meteostat_enhanced', 'create', [import_data])
        print(f"✅ Import Meteostat créé (ID: {import_id})")
        
        # ÉTAPE 3: Lancer l'import
        print("\n🚀 ÉTAPE 3: Lancer l'import des données...")
        
        result = models.execute_kw(db, uid, password, 'smart_agri_meteostat_enhanced', 'action_importer_donnees_reelles', [import_id])
        print("✅ Import lancé avec succès")
        
        # ÉTAPE 4: Vérifier les résultats
        print("\n📊 ÉTAPE 4: Vérifier les résultats...")
        
        import time
        time.sleep(3)  # Attendre le traitement
        
        import_result = models.execute_kw(db, uid, password, 'smart_agri_meteostat_enhanced', 'read', [import_id], 
                                       ['statut_import', 'nombre_enregistrements', 'log_import', 'erreur_import'])
        
        if import_result:
            result = import_result[0]
            print(f"📡 Statut de l'import: {result.get('statut_import', 'N/A')}")
            print(f"📈 Nombre d'enregistrements: {result.get('nombre_enregistrements', 'N/A')}")
            
            if result.get('log_import'):
                print(f"📋 Log d'import:")
                print(result['log_import'])
            
            if result.get('erreur_import'):
                print(f"❌ Erreur: {result['erreur_import']}")
        
        # ÉTAPE 5: Vérifier les données météo créées
        print("\n🌤️ ÉTAPE 5: Vérifier les données météo créées...")
        
        meteo_count = models.execute_kw(db, uid, password, 'smart_agri_meteo', 'search_count', 
                                      [[('exploitation_id', '=', exploitation_id)]])
        print(f"📊 Nombre de données météo: {meteo_count}")
        
        if meteo_count > 0:
            # Récupérer quelques données météo
            meteo_data = models.execute_kw(db, uid, password, 'smart_agri_meteo', 'search_read', 
                                         [[('exploitation_id', '=', exploitation_id)]], 
                                         {'fields': ['date_mesure', 'temperature', 'precipitation', 'humidite', 'source']}, 
                                         limit=5)
            
            print("🌡️ Dernières données météo:")
            for meteo in meteo_data:
                print(f"  📅 {meteo['date_mesure']}: {meteo['temperature']}°C, {meteo['precipitation']}mm, {meteo['humidite']}% ({meteo['source']})")
        
        print("\n🎉 IMPORT METEOSTAT TERMINÉ AVEC SUCCÈS !")
        print("\n📍 OÙ VOIR LES RÉSULTATS:")
        print("1. Menu '🌤️ Météo & Climat' > '📡 Meteostat Réel'")
        print("2. Menu '🌤️ Météo & Climat' > '🌡️ Données Météo'")
        print("3. Menu '🤖 Intelligence Artificielle' > '🚀 IA Avancée'")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

if __name__ == "__main__":
    guide_import_meteostat()
