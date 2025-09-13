#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour vérifier le module
"""

import xmlrpc.client

# Configuration Odoo
url = 'http://localhost:10020'
db = 'odoo123'
username = 'hajar'
password = 'hajar'

print("🔍 VÉRIFICATION DU MODULE")
print("=" * 30)

try:
    # Connexion
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    print(f"✅ Connexion réussie - UID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # Vérifier les modules disponibles
    print("\n🔍 Modules disponibles...")
    
    try:
        modules = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', 
                                   [['name', 'ilike', 'smart']], 
                                   {'fields': ['name', 'state', 'summary']})
        
        print(f"✅ Modules trouvés: {len(modules)}")
        for module in modules:
            print(f"   - {module['name']} ({module['state']}) - {module.get('summary', '')}")
    
    except Exception as e:
        print(f"❌ Erreur modules: {str(e)[:100]}...")
    
    # Vérifier les modèles disponibles
    print("\n🔍 Modèles disponibles...")
    
    try:
        models_list = models.execute_kw(db, uid, password, 'ir.model', 'search_read', 
                                       [['model', 'ilike', 'smart']], 
                                       {'fields': ['model', 'name']})
        
        print(f"✅ Modèles trouvés: {len(models_list)}")
        for model in models_list:
            print(f"   - {model['model']} - {model['name']}")
    
    except Exception as e:
        print(f"❌ Erreur modèles: {str(e)[:100]}...")
    
    print("\n" + "=" * 30)
    print("🎯 VÉRIFICATION TERMINÉE")
    
except Exception as e:
    print(f"❌ Erreur générale: {str(e)}")

print("\n🌐 Allez sur http://localhost:10020 pour installer le module manuellement")
