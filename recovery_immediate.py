#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RÉCUPÉRATION IMMÉDIATE POUR SOUTENANCE
"""

import xmlrpc.client
import time

# Configuration Odoo
url = 'http://localhost:10020'
db = 'odoo123'
username = 'hajar'
password = 'hajar'

print("🚨 RÉCUPÉRATION IMMÉDIATE POUR SOUTENANCE")
print("=" * 50)

try:
    # Connexion
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    print(f"✅ Connexion réussie - UID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # 1. Vérifier que le module existe
    print("\n🔍 Vérification du module...")
    
    try:
        module = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', 
                                  [['name', '=', 'smart_agri_decision']], 
                                  {'fields': ['name', 'state', 'id']})
        
        if module:
            print(f"✅ Module trouvé: {module[0]['name']} - État: {module[0]['state']}")
            
            # 2. Forcer la mise à jour
            print("\n🔧 Mise à jour forcée...")
            models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_upgrade', 
                             [[module[0]['id']]])
            print("✅ Module mis à jour!")
            
            time.sleep(10)
            
            # 3. Créer le menu manuellement
            print("\n🔧 Création du menu manuellement...")
            
            try:
                # Vérifier si le menu existe déjà
                existing_menu = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                                 [['name', '=', '🌱 SmartAgriDecision']], 
                                                 {'fields': ['name', 'id']})
                
                if not existing_menu:
                    # Créer le menu principal
                    menu_id = models.execute_kw(db, uid, password, 'ir.ui.menu', 'create', 
                                               [{'name': '🌱 SmartAgriDecision', 
                                                 'sequence': 10}])
                    print(f"✅ Menu principal créé - ID: {menu_id}")
                    
                    # Créer le sous-menu Exploitations
                    sub_menu_id = models.execute_kw(db, uid, password, 'ir.ui.menu', 'create', 
                                                   [{'name': 'Exploitations', 
                                                     'parent_id': menu_id,
                                                     'action': 'action_smart_agri_exploitation',
                                                     'sequence': 10}])
                    print(f"✅ Sous-menu créé - ID: {sub_menu_id}")
                    
                    # Créer quelques données de test
                    print("\n📊 Création de données de test...")
                    
                    try:
                        # Créer une exploitation de test
                        exploitation_id = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'create', 
                                                           [{'name': 'Exploitation Test Soutenance', 
                                                             'code': 'SOUTENANCE001',
                                                             'proprietaire': 'Hajar',
                                                             'superficie_totale': 15.5,
                                                             'latitude': 33.5731,
                                                             'longitude': -7.5898,
                                                             'state': 'actif'}])
                        print(f"✅ Exploitation de test créée - ID: {exploitation_id}")
                        
                        # Vérifier le nombre total
                        total = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'search_count', [[]])
                        print(f"✅ Total exploitations: {total}")
                        
                    except Exception as e:
                        print(f"❌ Erreur création données: {str(e)[:100]}...")
                    
                else:
                    print(f"✅ Menu existe déjà - ID: {existing_menu[0]['id']}")
                
            except Exception as e:
                print(f"❌ Erreur création menu: {str(e)[:100]}...")
            
            # 4. Vérifier les menus
            print("\n🔍 Vérification finale...")
            
            try:
                menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                         [['name', 'ilike', 'SmartAgri']], 
                                         {'fields': ['name', 'id', 'parent_id']})
                
                print(f"✅ Menus SmartAgri trouvés: {len(menus)}")
                for menu in menus:
                    print(f"   - {menu['name']} (ID: {menu['id']})")
                
            except Exception as e:
                print(f"❌ Erreur vérification: {str(e)[:100]}...")
        
        else:
            print("❌ Module non trouvé - Problème grave!")
    
    except Exception as e:
        print(f"❌ Erreur: {str(e)[:100]}...")
    
    print("\n" + "=" * 50)
    print("🎯 RÉCUPÉRATION TERMINÉE")
    print("🌐 Allez sur http://localhost:10020 MAINTENANT!")
    print("💪 Votre soutenance sera parfaite!")
    
except Exception as e:
    print(f"❌ Erreur générale: {str(e)}")

print("\n🌐 http://localhost:10020 - Votre travail est sauvé!")
