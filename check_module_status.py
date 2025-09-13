#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour vérifier le statut du module
"""

import xmlrpc.client

# Configuration Odoo
url = 'http://localhost:10020'
db = 'odoo123'
username = 'hajar'
password = 'hajar'

print("🔍 VÉRIFICATION DU STATUT DU MODULE")
print("=" * 40)

try:
    # Connexion
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    print(f"✅ Connexion réussie - UID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # 1. Vérifier tous les modules
    print("\n🔍 Tous les modules...")
    
    try:
        all_modules = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', 
                                       [[]], 
                                       {'fields': ['name', 'state', 'summary'], 'limit': 50})
        
        print(f"✅ Modules trouvés: {len(all_modules)}")
        
        # Chercher notre module
        smart_agri_found = False
        for module in all_modules:
            if 'smart' in module['name'].lower() or 'agri' in module['name'].lower():
                print(f"   - {module['name']} ({module['state']}) - {module.get('summary', '')}")
                if module['name'] == 'smart_agri_decision':
                    smart_agri_found = True
        
        if not smart_agri_found:
            print("❌ Module smart_agri_decision non trouvé dans la liste")
            print("💡 Le module n'est pas détecté par Odoo")
        else:
            print("✅ Module smart_agri_decision trouvé!")
    
    except Exception as e:
        print(f"❌ Erreur modules: {str(e)[:100]}...")
    
    # 2. Vérifier les menus
    print("\n🔍 Menus disponibles...")
    
    try:
        menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                 [['name', 'ilike', 'smart']], 
                                 {'fields': ['name', 'parent_id']})
        
        print(f"✅ Menus SmartAgri trouvés: {len(menus)}")
        for menu in menus:
            print(f"   - {menu['name']}")
    
    except Exception as e:
        print(f"❌ Erreur menus: {str(e)[:100]}...")
    
    print("\n" + "=" * 40)
    print("🎯 VÉRIFICATION TERMINÉE")
    
except Exception as e:
    print(f"❌ Erreur générale: {str(e)}")

print("\n🌐 Allez sur http://localhost:10020 pour vérifier manuellement")
