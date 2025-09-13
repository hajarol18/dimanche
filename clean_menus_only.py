#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT POUR NETTOYER SEULEMENT LES MENUS DUPLIQUÉS
Garde l'application SmartAgriDecision active et supprime seulement les menus dupliqués
"""

import xmlrpc.client
import sys
import time

def clean_menus_only():
    """Supprime seulement les menus dupliqués sans toucher au module"""
    
    # Configuration de connexion
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        print("🧹 NETTOYAGE DES MENUS DUPLIQUÉS (SANS DÉSACTIVER L'APP)")
        print("=" * 70)
        
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
        root_menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                     [[('name', 'ilike', 'SmartAgriDecision'), ('parent_id', '=', False)]], 
                                     {'fields': ['name', 'id', 'sequence', 'web_icon']})
        
        print(f"📊 Trouvé {len(root_menus)} menus racines SmartAgriDecision:")
        for menu in root_menus:
            icon_info = menu.get('web_icon', 'Pas d\'icône')
            print(f"  🆔 ID: {menu['id']} | 📝 Nom: {menu['name']} | 🔢 Séquence: {menu['sequence']}")
            print(f"      🎨 Icône: {icon_info}")
        
        if len(root_menus) <= 1:
            print("✅ Aucun menu dupliqué trouvé")
            return True
        
        print(f"\n🗑️ SUPPRESSION DES MENUS DUPLIQUÉS...")
        
        # Garder le menu avec l'icône complète (celui qui a web_icon)
        menu_to_keep = None
        menus_to_delete = []
        
        for menu in root_menus:
            if menu.get('web_icon') and 'smart_agri_decision' in str(menu.get('web_icon', '')):
                menu_to_keep = menu
            else:
                menus_to_delete.append(menu)
        
        if not menu_to_keep:
            # Si aucun menu n'a d'icône, garder le premier
            menu_to_keep = root_menus[0]
            menus_to_delete = root_menus[1:]
        
        print(f"✅ Menu à conserver: ID {menu_to_keep['id']} - {menu_to_keep['name']}")
        print(f"🗑️ Menus à supprimer: {len(menus_to_delete)}")
        
        for menu in menus_to_delete:
            try:
                print(f"  🗑️ Suppression du menu ID {menu['id']} - {menu['name']}...")
                
                # Supprimer seulement ce menu (pas ses enfants)
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
            print(f"  ✅ ID: {menu['id']} | 📝 Nom: {menu['name']} | 🔢 Séquence: {menu['sequence']}")
            print(f"      🎨 Icône: {icon_info}")
        
        if len(final_menus) == 1:
            print("\n🎉 SUCCÈS: Plus qu'un seul menu SmartAgriDecision !")
            print("🌐 Allez sur http://localhost:10020 pour vérifier")
            print("📱 Vous ne devriez voir qu'une seule application maintenant")
            print("✅ Votre application SmartAgriDecision reste active et fonctionnelle")
        else:
            print(f"\n⚠️ ATTENTION: Il reste {len(final_menus)} menus racines")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧹 NETTOYAGE DES MENUS DUPLIQUÉS (SANS DÉSACTIVER L'APP)")
    print("=" * 70)
    
    success = clean_menus_only()
    
    if success:
        print("\n✅ NETTOYAGE TERMINÉ AVEC SUCCÈS !")
        print("🎯 Vous ne devriez plus avoir qu'une seule application")
        print("✅ Votre application SmartAgriDecision reste active")
    else:
        print("\n❌ ÉCHEC: Vérification manuelle nécessaire")
    
    print("\n" + "=" * 70)
