#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour forcer l'installation du module
"""

import xmlrpc.client
import time

# Configuration Odoo
url = 'http://localhost:10020'
db = 'odoo123'
username = 'hajar'
password = 'hajar'

print("🚀 FORCE INSTALLATION DU MODULE")
print("=" * 40)

try:
    # Connexion
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    print(f"✅ Connexion réussie - UID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # 1. Vérifier l'état du module
    print("\n🔍 Vérification du module...")
    
    try:
        module = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', 
                                  [['name', '=', 'smart_agri_decision']], 
                                  {'fields': ['name', 'state', 'latest_version']})
        
        if module:
            print(f"✅ Module trouvé: {module[0]['name']} - État: {module[0]['state']}")
            
            # 2. Forcer la mise à jour
            print("\n🔧 Mise à jour forcée du module...")
            
            try:
                models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_upgrade', 
                                 [[module[0]['id']]])
                print("✅ Module mis à jour avec succès!")
                
                # 3. Attendre
                print("\n⏳ Attente...")
                time.sleep(10)
                
                # 4. Vérifier les menus
                print("\n🔍 Vérification des menus...")
                
                try:
                    menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                             [['name', 'ilike', 'SmartAgri']], 
                                             {'fields': ['name', 'parent_id', 'sequence']})
                    
                    print(f"✅ Menus trouvés: {len(menus)}")
                    for menu in menus:
                        parent_name = "Racine" if not menu['parent_id'] else f"Parent ID: {menu['parent_id'][0]}"
                        print(f"   - {menu['name']} (Séquence: {menu['sequence']}, {parent_name})")
                    
                    if len(menus) == 0:
                        print("❌ Aucun menu trouvé - Le module n'est pas correctement installé")
                        
                        # 5. Réinstaller complètement
                        print("\n🔄 Réinstallation complète...")
                        try:
                            # Désinstaller
                            models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_uninstall', 
                                             [[module[0]['id']]])
                            print("✅ Module désinstallé")
                            
                            time.sleep(5)
                            
                            # Réinstaller
                            models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_install', 
                                             [[module[0]['id']]])
                            print("✅ Module réinstallé")
                            
                        except Exception as e:
                            print(f"❌ Erreur réinstallation: {str(e)[:100]}...")
                    
                except Exception as e:
                    print(f"❌ Erreur vérification menus: {str(e)[:100]}...")
                
            except Exception as e:
                print(f"❌ Erreur mise à jour: {str(e)[:100]}...")
        else:
            print("❌ Module non trouvé")
    
    except Exception as e:
        print(f"❌ Erreur recherche: {str(e)[:100]}...")
    
    print("\n" + "=" * 40)
    print("🎯 INSTALLATION TERMINÉE")
    print("🌐 Allez sur http://localhost:10020 et vérifiez le menu")
    
except Exception as e:
    print(f"❌ Erreur générale: {str(e)}")

print("\n🌐 Allez sur http://localhost:10020 pour tester")
