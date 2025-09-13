#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DIAGNOSTIC SIMPLE POUR IDENTIFIER LE PROBLÈME
"""

import xmlrpc.client

# Configuration Odoo
url = 'http://localhost:10020'
db = 'odoo123'
username = 'hajar'
password = 'hajar'

print("🔍 DIAGNOSTIC SIMPLE")
print("=" * 30)

try:
    # Connexion
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    print(f"✅ Connexion réussie - UID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # 1. Test simple - compter les utilisateurs
    print("\n🔍 Test 1: Utilisateurs...")
    try:
        user_count = models.execute_kw(db, uid, password, 'res.users', 'search_count', [[]])
        print(f"✅ Utilisateurs: {user_count}")
    except Exception as e:
        print(f"❌ Erreur utilisateurs: {str(e)[:50]}...")
    
    # 2. Test simple - compter les modules
    print("\n🔍 Test 2: Modules...")
    try:
        module_count = models.execute_kw(db, uid, password, 'ir.module.module', 'search_count', [[]])
        print(f"✅ Modules: {module_count}")
    except Exception as e:
        print(f"❌ Erreur modules: {str(e)[:50]}...")
    
    # 3. Test simple - chercher notre module
    print("\n🔍 Test 3: Notre module...")
    try:
        our_module = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', 
                                      [['name', '=', 'smart_agri_decision']], 
                                      {'fields': ['name', 'state']})
        if our_module:
            print(f"✅ Module trouvé: {our_module[0]['name']} - État: {our_module[0]['state']}")
        else:
            print("❌ Module non trouvé")
    except Exception as e:
        print(f"❌ Erreur module: {str(e)[:50]}...")
    
    # 4. Test simple - compter les menus
    print("\n🔍 Test 4: Menus...")
    try:
        menu_count = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_count', [[]])
        print(f"✅ Menus: {menu_count}")
    except Exception as e:
        print(f"❌ Erreur menus: {str(e)[:50]}...")
    
    print("\n" + "=" * 30)
    print("🎯 DIAGNOSTIC TERMINÉ")
    
except Exception as e:
    print(f"❌ Erreur générale: {str(e)}")

print("\n🌐 Allez sur http://localhost:10020 pour vérifier manuellement")
