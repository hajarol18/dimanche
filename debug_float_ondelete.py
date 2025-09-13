#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour déboguer et corriger l'erreur Float ondelete
"""

import xmlrpc.client
import json

# Configuration Odoo
url = 'http://localhost:10020'
db = 'odoo123'
username = 'hajar'
password = 'hajar'

print("🔍 DÉBOGAGE DE L'ERREUR FLOAT ONDELETE")
print("=" * 50)

try:
    # Connexion
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    print(f"✅ Connexion réussie - UID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # 1. Chercher des données corrompues dans ir_model_data
    print("\n🔍 Recherche de données corrompues...")
    
    try:
        # Chercher des enregistrements avec des problèmes
        corrupted_data = models.execute_kw(db, uid, password, 'ir.model.data', 'search_read', 
                                          [['model', 'ilike', 'smart_agri']], 
                                          {'fields': ['name', 'model', 'res_id', 'module'], 'limit': 20})
        print(f"✅ Données trouvées: {len(corrupted_data)}")
        
        for data in corrupted_data:
            print(f"   - {data['name']} -> {data['model']} (ID: {data['res_id']}, Module: {data['module']})")
    
    except Exception as e:
        print(f"❌ Erreur données: {str(e)[:100]}...")
    
    # 2. Chercher des vues corrompues
    print("\n🔍 Recherche de vues corrompues...")
    
    try:
        views = models.execute_kw(db, uid, password, 'ir.ui.view', 'search_read', 
                                 [['model', 'ilike', 'smart_agri']], 
                                 {'fields': ['name', 'model', 'type', 'arch'], 'limit': 10})
        print(f"✅ Vues trouvées: {len(views)}")
        
        for view in views:
            print(f"   - {view['name']} ({view['type']}) -> {view['model']}")
            # Chercher des problèmes dans l'architecture
            if 'ondelete' in str(view.get('arch', '')) and 'Float' in str(view.get('arch', '')):
                print(f"     ⚠️ Vue suspecte détectée!")
    
    except Exception as e:
        print(f"❌ Erreur vues: {str(e)[:100]}...")
    
    # 3. Chercher des champs corrompus
    print("\n🔍 Recherche de champs corrompus...")
    
    try:
        fields = models.execute_kw(db, uid, password, 'ir.model.fields', 'search_read', 
                                  [['model', 'ilike', 'smart_agri']], 
                                  {'fields': ['name', 'model', 'ttype', 'relation'], 'limit': 20})
        print(f"✅ Champs trouvés: {len(fields)}")
        
        for field in fields:
            if field['ttype'] == 'float' and field.get('relation'):
                print(f"   - {field['name']} ({field['ttype']}) -> {field['model']} (Relation: {field['relation']})")
    
    except Exception as e:
        print(f"❌ Erreur champs: {str(e)[:100]}...")
    
    # 4. Essayer de supprimer les données corrompues
    print("\n🧹 Tentative de nettoyage...")
    
    try:
        # Supprimer les données orphelines
        models.execute_kw(db, uid, password, 'ir.model.data', 'unlink', 
                          [models.execute_kw(db, uid, password, 'ir.model.data', 'search', 
                                            [['model', 'ilike', 'smart_agri', 'res_id', '=', 0]])])
        print("✅ Données orphelines supprimées")
        
        # Supprimer les vues corrompues
        models.execute_kw(db, uid, password, 'ir.ui.view', 'unlink', 
                          [models.execute_kw(db, uid, password, 'ir.ui.view', 'search', 
                                            [['model', 'ilike', 'smart_agri', 'type', '=', 'qweb']])])
        print("✅ Vues QWeb supprimées")
        
    except Exception as e:
        print(f"❌ Erreur nettoyage: {str(e)[:100]}...")
    
    print("\n" + "=" * 50)
    print("🎯 DÉBOGAGE TERMINÉ")
    
except Exception as e:
    print(f"❌ Erreur générale: {str(e)}")

print("\n🌐 Allez sur http://localhost:10020 pour tester")
