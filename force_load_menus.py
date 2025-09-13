#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour forcer le chargement des menus
"""

import xmlrpc.client
import time

# Configuration Odoo
url = 'http://localhost:10020'
db = 'odoo123'
username = 'hajar'
password = 'hajar'

print("🔧 FORCE CHARGEMENT DES MENUS")
print("=" * 40)

try:
    # Connexion
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    print(f"✅ Connexion réussie - UID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # 1. Forcer la mise à jour du module
    print("\n🔧 Mise à jour forcée du module...")
    
    try:
        module = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', 
                                  [['name', '=', 'smart_agri_decision']], 
                                  {'fields': ['name', 'state', 'id']})
        
        if module:
            print(f"✅ Module trouvé: {module[0]['name']} - État: {module[0]['state']}")
            
            # Forcer la mise à jour
            models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_upgrade', 
                             [[module[0]['id']]])
            print("✅ Module mis à jour!")
            
            # Attendre
            time.sleep(10)
            
            # 2. Vérifier les menus
            print("\n🔍 Vérification des menus...")
            
            try:
                # Chercher le menu principal
                main_menu = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                             [['name', '=', '🌱 SmartAgriDecision']], 
                                             {'fields': ['name', 'id', 'parent_id']})
                
                if main_menu:
                    print(f"✅ Menu principal trouvé: {main_menu[0]['name']} (ID: {main_menu[0]['id']})")
                    
                    # Chercher les sous-menus
                    sub_menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                                 [['parent_id', '=', main_menu[0]['id']]], 
                                                 {'fields': ['name', 'id', 'sequence']})
                    
                    print(f"✅ Sous-menus trouvés: {len(sub_menus)}")
                    for menu in sub_menus:
                        print(f"   - {menu['name']} (Séquence: {menu['sequence']})")
                    
                    if len(sub_menus) == 0:
                        print("❌ Aucun sous-menu trouvé - Problème de chargement")
                        
                        # 3. Créer manuellement le menu principal
                        print("\n🔧 Création manuelle du menu...")
                        
                        try:
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
                            
                        except Exception as e:
                            print(f"❌ Erreur création menu: {str(e)[:100]}...")
                    else:
                        print("✅ Menus chargés correctement!")
                
                else:
                    print("❌ Menu principal non trouvé - Problème de chargement")
            
            except Exception as e:
                print(f"❌ Erreur vérification menus: {str(e)[:100]}...")
        
        else:
            print("❌ Module non trouvé")
    
    except Exception as e:
        print(f"❌ Erreur mise à jour: {str(e)[:100]}...")
    
    print("\n" + "=" * 40)
    print("🎯 CHARGEMENT TERMINÉ")
    print("🌐 Allez sur http://localhost:10020 et vérifiez le menu")
    
except Exception as e:
    print(f"❌ Erreur générale: {str(e)}")

print("\n🌐 Allez sur http://localhost:10020 pour tester")
