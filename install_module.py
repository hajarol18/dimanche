#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour installer le module SmartAgriDecision
"""

import xmlrpc.client
import time

# Configuration Odoo
url = 'http://localhost:10020'
db = 'odoo123'
username = 'hajar'
password = 'hajar'

print("🚀 INSTALLATION DU MODULE SMARTAGRIDECISION")
print("=" * 50)

try:
    # Connexion
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    print(f"✅ Connexion réussie - UID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # 1. Vérifier si le module existe
    print("\n🔍 Vérification du module...")
    
    try:
        module = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', 
                                  [['name', '=', 'smart_agri_decision']], 
                                  {'fields': ['name', 'state', 'latest_version']})
        
        if module:
            print(f"✅ Module trouvé: {module[0]['name']} - État: {module[0]['state']}")
            
            # 2. Installer le module
            print("\n🔧 Installation du module...")
            
            try:
                models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_install', 
                                 [[module[0]['id']]])
                print("✅ Module installé avec succès!")
                
                # 3. Attendre que l'installation se termine
                print("\n⏳ Attente de l'installation...")
                time.sleep(10)
                
                # 4. Vérifier l'installation
                print("\n🔍 Vérification de l'installation...")
                
                try:
                    # Vérifier que le modèle existe
                    count = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'search_count', [[]])
                    print(f"✅ Modèle smart_agri_exploitation créé - {count} enregistrements")
                    
                    # Vérifier les menus
                    menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                             [['name', 'ilike', 'SmartAgri']], 
                                             {'fields': ['name', 'parent_id']})
                    print(f"✅ Menus créés: {len(menus)}")
                    for menu in menus:
                        print(f"   - {menu['name']}")
                    
                except Exception as e:
                    print(f"❌ Erreur vérification: {str(e)[:100]}...")
                
            except Exception as e:
                print(f"❌ Erreur installation: {str(e)[:100]}...")
        else:
            print("❌ Module non trouvé")
    
    except Exception as e:
        print(f"❌ Erreur recherche: {str(e)[:100]}...")
    
    print("\n" + "=" * 50)
    print("🎯 INSTALLATION TERMINÉE")
    print("🌐 Allez sur http://localhost:10020 pour voir le module")
    
except Exception as e:
    print(f"❌ Erreur générale: {str(e)}")

print("\n🌐 Allez sur http://localhost:10020 pour tester")
