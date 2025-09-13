#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUPPRESSION DU MENU EXPLOITATION DUPLIQUÉ
Supprime le menu sans icône (ID 283) et garde celui avec icône (ID 249)
"""

import xmlrpc.client

def supprimer_menu_duplique():
    """Supprime le menu exploitation dupliqué"""
    
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        print("🗑️ SUPPRESSION DU MENU EXPLOITATION DUPLIQUÉ")
        print("=" * 60)
        print("🎯 Suppression du menu sans icône (ID 283)")
        print("🎯 Conservation du menu avec icône 🏡 (ID 249)")
        print("=" * 60)
        
        # Connexion
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        print("✅ Connecté à Odoo")
        
        # 1. VÉRIFIER LES MENUS AVANT SUPPRESSION
        print("\n📋 ÉTAT AVANT SUPPRESSION")
        print("-" * 40)
        
        menus_avant = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                      [[('name', 'ilike', 'Exploitation')]], 
                                      {'fields': ['name', 'id', 'parent_id', 'sequence', 'web_icon']})
        
        for menu in menus_avant:
            parent_id = menu.get('parent_id', [0])[0] if menu.get('parent_id') else 0
            icone = "🏡" if "🏡" in menu['name'] else "❌"
            print(f"  - ID {menu['id']}: '{menu['name']}' - Parent: {parent_id} - Icône: {icone}")
        
        # 2. SUPPRIMER LE MENU SANS ICÔNE (ID 283)
        print(f"\n🗑️ SUPPRESSION DU MENU SANS ICÔNE")
        print("-" * 40)
        
        try:
            # Supprimer le menu ID 283 (sans icône)
            models.execute_kw(db, uid, password, 'ir.ui.menu', 'unlink', [283])
            print("  ✅ Menu ID 283 supprimé avec succès")
        except Exception as e:
            print(f"  ❌ Erreur lors de la suppression ID 283: {str(e)}")
            
            # Essayer de supprimer par nom
            try:
                menu_sans_icone = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search', 
                                                  [[('name', '=', 'Exploitations'), ('id', '!=', 249)]])
                if menu_sans_icone:
                    models.execute_kw(db, uid, password, 'ir.ui.menu', 'unlink', menu_sans_icone)
                    print("  ✅ Menu sans icône supprimé par nom")
                else:
                    print("  ℹ️ Aucun menu sans icône trouvé")
            except Exception as e2:
                print(f"  ❌ Erreur lors de la suppression par nom: {str(e2)}")
        
        # 3. VÉRIFIER LE RÉSULTAT APRÈS SUPPRESSION
        print(f"\n✅ ÉTAT APRÈS SUPPRESSION")
        print("-" * 40)
        
        menus_apres = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                      [[('name', 'ilike', 'Exploitation')]], 
                                      {'fields': ['name', 'id', 'parent_id', 'sequence', 'web_icon']})
        
        print(f"  📋 Menus Exploitation restants: {len(menus_apres)}")
        
        for menu in menus_apres:
            parent_id = menu.get('parent_id', [0])[0] if menu.get('parent_id') else 0
            icone = "🏡" if "🏡" in menu['name'] else "❌"
            print(f"  - ID {menu['id']}: '{menu['name']}' - Parent: {parent_id} - Icône: {icone}")
        
        # 4. RÉSULTAT FINAL
        print(f"\n🎉 RÉSULTAT FINAL")
        print("=" * 40)
        
        if len(menus_apres) == 1:
            print("  ✅ SUCCÈS: Un seul menu Exploitation restant")
            print("  ✅ Le menu avec icône 🏡 a été conservé")
            print("  ✅ Le menu dupliqué a été supprimé")
        elif len(menus_apres) == 0:
            print("  ⚠️ ATTENTION: Aucun menu Exploitation restant")
            print("  ℹ️ Il faudra recréer le menu")
        else:
            print(f"  ⚠️ ATTENTION: {len(menus_apres)} menus Exploitation restants")
            print("  ℹ️ Vérifiez manuellement dans l'interface Odoo")
        
        print(f"\n🌐 Vérifiez le résultat sur: http://localhost:10020")
        print(f"📋 Le menu Exploitation devrait maintenant être unique avec l'icône 🏡")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {str(e)}")
        return False

if __name__ == "__main__":
    supprimer_menu_duplique()
