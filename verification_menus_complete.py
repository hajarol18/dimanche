#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VÉRIFICATION COMPLÈTE DES MENUS
Analyse de tous les sous-menus du module SmartAgriDecision
"""

import xmlrpc.client

def verification_menus_complete():
    """Vérification complète de tous les menus"""
    
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        print("🔍 VÉRIFICATION COMPLÈTE DES MENUS")
        print("=" * 60)
        print("🎯 Analyse de tous les sous-menus du module")
        print("=" * 60)
        
        # Connexion
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        print("✅ Connecté à Odoo")
        
        # 1. VÉRIFIER LE MENU RACINE
        print("\n🌾 MENU RACINE")
        print("-" * 40)
        
        menu_racine = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                      [[('name', '=', '🌾 SmartAgriDecision')]], 
                                      {'fields': ['name', 'id', 'sequence']})
        
        if menu_racine:
            print(f"  ✅ Menu racine trouvé: ID {menu_racine[0]['id']}")
            racine_id = menu_racine[0]['id']
        else:
            print("  ❌ Menu racine non trouvé")
            return False
        
        # 2. VÉRIFIER TOUS LES SOUS-MENUS PRINCIPAUX
        print("\n📊 SOUS-MENUS PRINCIPAUX")
        print("-" * 40)
        
        sous_menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                     [[('parent_id', '=', racine_id)]], 
                                     {'fields': ['name', 'id', 'sequence', 'web_icon']})
        
        sous_menus.sort(key=lambda x: x.get('sequence', 0))
        
        for menu in sous_menus:
            icone = menu.get('web_icon', '❌')
            print(f"  {menu.get('sequence', 0):2d}. {menu['name']} (ID: {menu['id']}) - Icône: {icone}")
        
        # 3. VÉRIFIER LES SOUS-MENUS DE CHAQUE SECTION
        print("\n🔍 DÉTAIL DES SOUS-MENUS PAR SECTION")
        print("-" * 60)
        
        for section in sous_menus:
            print(f"\n📁 {section['name']} (ID: {section['id']})")
            print("-" * 40)
            
            # Récupérer les sous-menus de cette section
            sous_sous_menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                              [[('parent_id', '=', section['id'])]], 
                                              {'fields': ['name', 'id', 'sequence', 'action', 'web_icon']})
            
            sous_sous_menus.sort(key=lambda x: x.get('sequence', 0))
            
            if sous_sous_menus:
                for sous_menu in sous_sous_menus:
                    action = sous_menu.get('action', 'N/A')
                    icone = sous_menu.get('web_icon', '❌')
                    print(f"    {sous_menu.get('sequence', 0):2d}. {sous_menu['name']} (ID: {sous_menu['id']})")
                    print(f"        Action: {action} | Icône: {icone}")
            else:
                print("    Aucun sous-menu trouvé")
        
        # 4. VÉRIFIER SPÉCIFIQUEMENT LES MENUS EXPLOITATION
        print("\n🏡 VÉRIFICATION SPÉCIFIQUE DES MENUS EXPLOITATION")
        print("-" * 60)
        
        menus_exploitation = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                             [[('name', 'ilike', 'Exploitation')]], 
                                             {'fields': ['name', 'id', 'parent_id', 'sequence', 'web_icon', 'action']})
        
        print(f"  📋 Menus Exploitation trouvés: {len(menus_exploitation)}")
        
        for menu in menus_exploitation:
            parent_id = menu.get('parent_id', [0])[0] if menu.get('parent_id') else 0
            icone = "🏡" if "🏡" in menu['name'] else "❌"
            action = menu.get('action', 'N/A')
            print(f"    - ID {menu['id']}: '{menu['name']}'")
            print(f"      Parent: {parent_id} | Icône: {icone} | Action: {action}")
        
        # 5. RÉSUMÉ DE LA VÉRIFICATION
        print("\n✅ RÉSUMÉ DE LA VÉRIFICATION")
        print("=" * 60)
        
        if len(menus_exploitation) == 1:
            print("  ✅ SUCCÈS: Un seul menu Exploitation trouvé")
            print("  ✅ Le problème des menus dupliqués est résolu")
        elif len(menus_exploitation) == 0:
            print("  ⚠️ ATTENTION: Aucun menu Exploitation trouvé")
            print("  ℹ️ Il faudra vérifier la configuration")
        else:
            print(f"  ❌ PROBLÈME: {len(menus_exploitation)} menus Exploitation trouvés")
            print("  ℹ️ Il y a encore des menus dupliqués")
        
        # 6. STATISTIQUES FINALES
        print(f"\n📊 STATISTIQUES FINALES")
        print("-" * 40)
        
        total_menus = len(models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_count', 
                                          [[('name', 'ilike', 'SmartAgri')]]))
        
        print(f"  🌾 Menus racine: 1")
        print(f"  📁 Sous-menus principaux: {len(sous_menus)}")
        print(f"  📋 Total menus SmartAgri: {total_menus}")
        print(f"  🏡 Menus Exploitation: {len(menus_exploitation)}")
        
        print(f"\n🎉 VÉRIFICATION TERMINÉE !")
        print(f"🌐 Vérifiez le résultat sur: http://localhost:10020")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {str(e)}")
        return False

if __name__ == "__main__":
    verification_menus_complete()
