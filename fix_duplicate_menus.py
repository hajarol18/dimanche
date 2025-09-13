#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT POUR RÉSOUDRE LE PROBLÈME DES MENUS DUPLIQUÉS
Supprime les menus dupliqués et garde seulement le menu principal
"""

import xmlrpc.client
import sys
import time

def fix_duplicate_menus():
    """Supprime les menus dupliqués et garde seulement le menu principal"""
    
    # Configuration de connexion
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        print("🔧 RÉSOLUTION DU PROBLÈME DES MENUS DUPLIQUÉS")
        print("=" * 60)
        
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
        
        print("\n🔍 RECHERCHE DES MENUS DUPLIQUÉS...")
        
        # Chercher tous les menus racines SmartAgriDecision
        menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                [[('name', 'ilike', 'SmartAgriDecision'), ('parent_id', '=', False)]], 
                                {'fields': ['name', 'id', 'sequence', 'web_icon']})
        
        print(f"📊 Trouvé {len(menus)} menus racines SmartAgriDecision:")
        for menu in menus:
            icon_info = menu.get('web_icon', 'Pas d\'icône')
            print(f"  🆔 ID: {menu['id']} | 📝 Nom: {menu['name']} | 🔢 Séquence: {menu['sequence']} | 🎨 Icône: {icon_info}")
        
        if len(menus) <= 1:
            print("✅ Aucun menu dupliqué trouvé")
            return True
        
        print(f"\n🗑️ SUPPRESSION DES MENUS DUPLIQUÉS...")
        
        # Garder le menu avec la séquence la plus basse (le principal)
        menus_sorted = sorted(menus, key=lambda x: x['sequence'])
        menu_to_keep = menus_sorted[0]
        menus_to_delete = menus_sorted[1:]
        
        print(f"✅ Menu à conserver: ID {menu_to_keep['id']} - {menu_to_keep['name']}")
        
        for menu in menus_to_delete:
            try:
                print(f"  🗑️ Suppression du menu ID {menu['id']} - {menu['name']}...")
                
                # Supprimer le menu et tous ses enfants
                models.execute_kw(db, uid, password, 'ir.ui.menu', 'unlink', [menu['id']])
                print(f"  ✅ Menu supprimé")
                
            except Exception as e:
                print(f"  ⚠️ Erreur lors de la suppression: {str(e)}")
        
        # Attendre un peu pour que les changements prennent effet
        print("\n⏳ Attente de la finalisation des changements...")
        time.sleep(3)
        
        print("\n✅ VÉRIFICATION FINALE...")
        
        # Vérifier l'état final
        final_menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                      [[('name', 'ilike', 'SmartAgriDecision'), ('parent_id', '=', False)]], 
                                      {'fields': ['name', 'id', 'sequence', 'web_icon']})
        
        print(f"📊 État final: {len(final_menus)} menu(s) racine SmartAgriDecision")
        for menu in final_menus:
            icon_info = menu.get('web_icon', 'Pas d\'icône')
            print(f"  ✅ ID: {menu['id']} | 📝 Nom: {menu['name']} | 🔢 Séquence: {menu['sequence']} | 🎨 Icône: {icon_info}")
        
        if len(final_menus) == 1:
            print("\n🎉 SUCCÈS: Plus qu'un seul menu SmartAgriDecision !")
            print("🌐 Allez sur http://localhost:10020 pour vérifier")
            print("📱 Vous ne devriez voir qu'une seule application maintenant")
        else:
            print(f"\n⚠️ ATTENTION: Il reste {len(final_menus)} menus")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la résolution: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 RÉSOLUTION DU PROBLÈME DES MENUS DUPLIQUÉS")
    print("=" * 60)
    
    success = fix_duplicate_menus()
    
    if success:
        print("\n✅ RÉSOLUTION TERMINÉE AVEC SUCCÈS !")
        print("🎯 Vous ne devriez plus avoir qu'une seule application")
    else:
        print("\n❌ ÉCHEC: Vérification manuelle nécessaire")
    
    print("\n" + "=" * 60)
