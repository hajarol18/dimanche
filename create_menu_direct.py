#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CRÉATION DIRECTE DU MENU DANS LA BASE DE DONNÉES
"""

import xmlrpc.client
import time

# Configuration Odoo
url = 'http://localhost:10020'
db = 'odoo123'
username = 'hajar'
password = 'hajar'

print("🔧 CRÉATION DIRECTE DU MENU")
print("=" * 40)

try:
    # Connexion
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    print(f"✅ Connexion réussie - UID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # 1. Vérifier si le menu existe déjà
    print("\n🔍 Vérification du menu existant...")
    
    try:
        existing_menu = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                         [['name', '=', '🌱 SmartAgriDecision']], 
                                         {'fields': ['name', 'id']})
        
        if existing_menu:
            print(f"✅ Menu existe déjà - ID: {existing_menu[0]['id']}")
            menu_id = existing_menu[0]['id']
        else:
            print("❌ Menu n'existe pas - Création...")
            
            # 2. Créer le menu principal
            menu_id = models.execute_kw(db, uid, password, 'ir.ui.menu', 'create', 
                                       [{'name': '🌱 SmartAgriDecision', 
                                         'sequence': 5}])
            print(f"✅ Menu principal créé - ID: {menu_id}")
        
        # 3. Créer le sous-menu Exploitations
        print("\n🔧 Création du sous-menu Exploitations...")
        
        try:
            # Vérifier si le sous-menu existe
            existing_submenu = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                                [['name', '=', 'Exploitations', 'parent_id', '=', menu_id]], 
                                                {'fields': ['name', 'id']})
            
            if existing_submenu:
                print(f"✅ Sous-menu existe déjà - ID: {existing_submenu[0]['id']}")
            else:
                # Créer le sous-menu
                submenu_id = models.execute_kw(db, uid, password, 'ir.ui.menu', 'create', 
                                              [{'name': 'Exploitations', 
                                                'parent_id': menu_id,
                                                'action': 'action_smart_agri_exploitation',
                                                'sequence': 10}])
                print(f"✅ Sous-menu créé - ID: {submenu_id}")
                
        except Exception as e:
            print(f"❌ Erreur sous-menu: {str(e)[:100]}...")
        
        # 4. Vérifier les menus
        print("\n🔍 Vérification finale...")
        
        try:
            menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                     [['name', 'ilike', 'SmartAgri']], 
                                     {'fields': ['name', 'id', 'parent_id']})
            
            print(f"✅ Menus SmartAgri trouvés: {len(menus)}")
            for menu in menus:
                parent_info = "Racine" if not menu['parent_id'] else f"Parent: {menu['parent_id'][0]}"
                print(f"   - {menu['name']} (ID: {menu['id']}, {parent_info})")
            
            if len(menus) > 0:
                print("\n🎉 SUCCÈS! Votre menu est créé!")
                print("🌐 Allez sur http://localhost:10020 pour voir le menu")
            else:
                print("\n❌ Aucun menu trouvé")
                
        except Exception as e:
            print(f"❌ Erreur vérification: {str(e)[:100]}...")
    
    except Exception as e:
        print(f"❌ Erreur: {str(e)[:100]}...")
    
    print("\n" + "=" * 40)
    print("🎯 CRÉATION TERMINÉE")
    
except Exception as e:
    print(f"❌ Erreur générale: {str(e)}")

print("\n🌐 Allez sur http://localhost:10020 pour voir votre menu!")
