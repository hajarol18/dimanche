#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour corriger l'erreur Float ondelete
"""

import xmlrpc.client

# Configuration Odoo
url = 'http://localhost:10020'
db = 'odoo123'
username = 'hajar'
password = 'hajar'

print("🔧 CORRECTION DE L'ERREUR FLOAT ONDELETE")
print("=" * 50)

try:
    # Connexion
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    print(f"✅ Connexion réussie - UID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # 1. Vérifier l'état du module
    print("\n📋 Vérification du module...")
    try:
        module = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', 
                                  [['name', '=', 'smart_agri_decision']], 
                                  {'fields': ['name', 'state', 'latest_version']})
        if module:
            print(f"✅ Module: {module[0]['name']} - État: {module[0]['state']} - Version: {module[0].get('latest_version', 'N/A')}")
        else:
            print("❌ Module non trouvé")
    except Exception as e:
        print(f"❌ Erreur module: {str(e)[:100]}...")
    
    # 2. Vérifier les données corrompues
    print("\n🔍 Recherche de données corrompues...")
    try:
        # Chercher des enregistrements avec des problèmes
        corrupted_data = models.execute_kw(db, uid, password, 'ir.model.data', 'search_read', 
                                          [['model', 'ilike', 'smart_agri']], 
                                          {'fields': ['name', 'model', 'res_id'], 'limit': 10})
        print(f"✅ Données trouvées: {len(corrupted_data)}")
        for data in corrupted_data[:5]:
            print(f"   - {data['name']} -> {data['model']} (ID: {data['res_id']})")
    except Exception as e:
        print(f"❌ Erreur données: {str(e)[:100]}...")
    
    # 3. Essayer de nettoyer le cache
    print("\n🧹 Nettoyage du cache...")
    try:
        # Forcer la mise à jour du module
        models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_upgrade', 
                          [models.execute_kw(db, uid, password, 'ir.module.module', 'search', 
                                            [['name', '=', 'smart_agri_decision']])])
        print("✅ Mise à jour du module lancée")
    except Exception as e:
        print(f"❌ Erreur mise à jour: {str(e)[:100]}...")
    
    print("\n" + "=" * 50)
    print("🎯 CORRECTION TERMINÉE")
    
except Exception as e:
    print(f"❌ Erreur générale: {str(e)}")

print("\n🌐 Allez sur http://localhost:10020 pour tester")
