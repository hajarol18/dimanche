#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT D'INVESTIGATION POUR COMPRENDRE LE PROBLÈME DES APPLICATIONS DUPLIQUÉES
Analyse en détail tous les menus et applications
"""

import xmlrpc.client
import sys
import time

def investigate_duplicate_apps():
    """Investigation complète du problème des applications dupliquées"""
    
    # Configuration de connexion
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        print("🔍 INVESTIGATION COMPLÈTE DU PROBLÈME DES APPLICATIONS DUPLIQUÉES")
        print("=" * 80)
        
        # Connexion à Odoo
        print("🔌 Connexion à Odoo...")
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if not uid:
            print("❌ Échec de l'authentification")
            return False
        
        print(f"✅ Connecté avec l'utilisateur ID: {uid}")
        
        # Connexion aux modèles
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        print("\n🔍 ANALYSE COMPLÈTE DES APPLICATIONS...")
        
        # 1. Vérifier tous les modules installés
        print("\n📦 MODULES INSTALLÉS:")
        installed_modules = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', 
                                            [[('state', '=', 'installed')]], 
                                            {'fields': ['name', 'application', 'category_id']})
        
        app_modules = [m for m in installed_modules if m.get('application')]
        print(f"📱 Modules applications: {len(app_modules)}")
        for module in app_modules:
            print(f"  📱 {module['name']} - Catégorie: {module.get('category_id', 'N/A')}")
        
        # 2. Vérifier tous les menus racines
        print("\n🌳 TOUS LES MENUS RACINES:")
        all_root_menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                         [[('parent_id', '=', False)]], 
                                         {'fields': ['name', 'id', 'sequence', 'web_icon', 'action']})
        
        print(f"📊 Total menus racines: {len(all_root_menus)}")
        for menu in all_root_menus:
            icon_info = menu.get('web_icon', 'Pas d\'icône')
            action_info = menu.get('action', 'Pas d\'action')
            print(f"  🆔 ID: {menu['id']} | 📝 Nom: {menu['name']} | 🔢 Séquence: {menu['sequence']}")
            print(f"      🎨 Icône: {icon_info}")
            print(f"      ⚡ Action: {action_info}")
            print()
        
        # 3. Vérifier spécifiquement les menus SmartAgriDecision
        print("\n🌾 MENUS SMARTAGRIDECISION:")
        smart_agri_menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                           [[('name', 'ilike', 'SmartAgriDecision')]], 
                                           {'fields': ['name', 'id', 'parent_id', 'sequence', 'web_icon', 'action']})
        
        root_smart_agri = [m for m in smart_agri_menus if not m.get('parent_id')]
        child_smart_agri = [m for m in smart_agri_menus if m.get('parent_id')]
        
        print(f"🌳 Menus racines SmartAgriDecision: {len(root_smart_agri)}")
        for menu in root_smart_agri:
            icon_info = menu.get('web_icon', 'Pas d\'icône')
            action_info = menu.get('action', 'Pas d\'action')
            print(f"  🆔 ID: {menu['id']} | 📝 Nom: {menu['name']} | 🔢 Séquence: {menu['sequence']}")
            print(f"      🎨 Icône: {icon_info}")
            print(f"      ⚡ Action: {action_info}")
            print()
        
        print(f"🌿 Sous-menus SmartAgriDecision: {len(child_smart_agri)}")
        
        # 4. Vérifier les actions liées aux menus
        print("\n⚡ ACTIONS LIÉES AUX MENUS SMARTAGRIDECISION:")
        for menu in root_smart_agri:
            if menu.get('action'):
                try:
                    action = models.execute_kw(db, uid, password, 'ir.actions.act_window', 'read', 
                                             [menu['action']], ['name', 'res_model', 'view_mode'])
                    print(f"  Menu ID {menu['id']} -> Action: {action}")
                except Exception as e:
                    print(f"  Menu ID {menu['id']} -> Erreur action: {str(e)}")
        
        # 5. Vérifier les données XML chargées
        print("\n📄 VÉRIFICATION DES DONNÉES XML CHARGÉES:")
        try:
            # Chercher les enregistrements de menu dans ir.model.data
            menu_data = models.execute_kw(db, uid, password, 'ir.model.data', 'search_read', 
                                        [[('model', '=', 'ir.ui.menu'), ('name', 'ilike', 'smart_agri')]], 
                                        {'fields': ['name', 'module', 'res_id', 'noupdate']})
            
            print(f"📊 Données XML de menus SmartAgri: {len(menu_data)}")
            for data in menu_data:
                print(f"  📄 {data['name']} - Module: {data['module']} - Res ID: {data['res_id']} - NoUpdate: {data['noupdate']}")
        except Exception as e:
            print(f"  ⚠️ Erreur lors de la vérification des données XML: {str(e)}")
        
        # 6. Recommandations
        print("\n💡 RECOMMANDATIONS:")
        if len(root_smart_agri) > 1:
            print("  ❌ PROBLÈME: Plusieurs menus racines SmartAgriDecision détectés")
            print("  🔧 SOLUTION: Supprimer les menus dupliqués")
            
            # Identifier le menu à garder (celui avec l'icône)
            menu_to_keep = None
            for menu in root_smart_agri:
                if menu.get('web_icon') and 'smart_agri_decision' in str(menu.get('web_icon', '')):
                    menu_to_keep = menu
                    break
            
            if menu_to_keep:
                print(f"  ✅ Menu à conserver: ID {menu_to_keep['id']} - {menu_to_keep['name']}")
                menus_to_delete = [m for m in root_smart_agri if m['id'] != menu_to_keep['id']]
                print(f"  🗑️ Menus à supprimer: {[m['id'] for m in menus_to_delete]}")
            else:
                print("  ⚠️ Aucun menu avec icône trouvé, garder le premier")
        else:
            print("  ✅ Aucun problème de duplication détecté")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'investigation: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 INVESTIGATION COMPLÈTE DU PROBLÈME DES APPLICATIONS DUPLIQUÉES")
    print("=" * 80)
    
    success = investigate_duplicate_apps()
    
    if success:
        print("\n✅ INVESTIGATION TERMINÉE")
    else:
        print("\n❌ ÉCHEC DE L'INVESTIGATION")
    
    print("\n" + "=" * 80)
