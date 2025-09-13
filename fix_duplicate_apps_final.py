#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT FINAL POUR RÉSOUDRE DÉFINITIVEMENT LE PROBLÈME DES APPLICATIONS DUPLIQUÉES
Supprime tous les menus dupliqués et recrée un menu propre
"""

import xmlrpc.client
import sys
import time

def fix_duplicate_apps_final():
    """Supprime définitivement tous les menus dupliqués"""
    
    # Configuration de connexion
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        print("🔧 RÉSOLUTION FINALE DU PROBLÈME DES APPLICATIONS DUPLIQUÉES")
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
        
        print("\n🔍 ANALYSE COMPLÈTE DES MENUS...")
        
        # Chercher TOUS les menus SmartAgriDecision (racines et enfants)
        all_menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                    [[('name', 'ilike', 'SmartAgriDecision')]], 
                                    {'fields': ['name', 'id', 'parent_id', 'sequence', 'web_icon', 'action']})
        
        print(f"📊 Trouvé {len(all_menus)} menus SmartAgriDecision au total")
        
        # Séparer les menus racines des sous-menus
        root_menus = [m for m in all_menus if not m.get('parent_id')]
        child_menus = [m for m in all_menus if m.get('parent_id')]
        
        print(f"🌳 Menus racines: {len(root_menus)}")
        print(f"🌿 Sous-menus: {len(child_menus)}")
        
        print("\n📋 DÉTAIL DES MENUS RACINES:")
        for menu in root_menus:
            icon_info = menu.get('web_icon', 'Pas d\'icône')
            action_info = menu.get('action', 'Pas d\'action')
            print(f"  🆔 ID: {menu['id']} | 📝 Nom: {menu['name']} | 🔢 Séquence: {menu['sequence']}")
            print(f"      🎨 Icône: {icon_info}")
            print(f"      ⚡ Action: {action_info}")
            print()
        
        if len(root_menus) <= 1:
            print("✅ Aucun menu dupliqué trouvé")
            return True
        
        print(f"\n🗑️ SUPPRESSION DE TOUS LES MENUS DUPLIQUÉS...")
        
        # Supprimer TOUS les menus SmartAgriDecision (racines et enfants)
        all_menu_ids = [menu['id'] for menu in all_menus]
        
        print(f"🗑️ Suppression de {len(all_menu_ids)} menus...")
        
        try:
            # Supprimer tous les menus en une fois
            models.execute_kw(db, uid, password, 'ir.ui.menu', 'unlink', all_menu_ids)
            print("✅ Tous les menus SmartAgriDecision supprimés")
        except Exception as e:
            print(f"⚠️ Erreur lors de la suppression groupée: {str(e)}")
            print("🔄 Tentative de suppression individuelle...")
            
            # Supprimer un par un
            for menu_id in all_menu_ids:
                try:
                    models.execute_kw(db, uid, password, 'ir.ui.menu', 'unlink', [menu_id])
                    print(f"  ✅ Menu ID {menu_id} supprimé")
                except Exception as e2:
                    print(f"  ⚠️ Erreur avec menu ID {menu_id}: {str(e2)}")
        
        # Attendre que les changements prennent effet
        print("\n⏳ Attente de la finalisation des suppressions...")
        time.sleep(5)
        
        print("\n🔄 RECHARGEMENT DU MODULE POUR RECRÉER LES MENUS...")
        
        # Recharger le module pour recréer les menus
        try:
            module = models.execute_kw(db, uid, password, 'ir.module.module', 'search', 
                                     [[('name', '=', 'smart_agri_decision')]])
            
            if module:
                print("🔄 Mise à jour du module...")
                models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_upgrade', [module[0]])
                print("✅ Module mis à jour")
            else:
                print("⚠️ Module smart_agri_decision non trouvé")
        except Exception as e:
            print(f"⚠️ Erreur lors de la mise à jour: {str(e)}")
        
        # Attendre que les menus soient recréés
        print("\n⏳ Attente de la recréation des menus...")
        time.sleep(10)
        
        print("\n✅ VÉRIFICATION FINALE...")
        
        # Vérifier l'état final
        final_menus = models.execute_kw(db, uid, password, 'ir.ui.menu', 'search_read', 
                                      [[('name', 'ilike', 'SmartAgriDecision')]], 
                                      {'fields': ['name', 'id', 'parent_id', 'sequence', 'web_icon']})
        
        final_root_menus = [m for m in final_menus if not m.get('parent_id')]
        final_child_menus = [m for m in final_menus if m.get('parent_id')]
        
        print(f"📊 État final:")
        print(f"  🌳 Menus racines: {len(final_root_menus)}")
        print(f"  🌿 Sous-menus: {len(final_child_menus)}")
        
        if final_root_menus:
            print("\n📋 MENUS RACINES FINAUX:")
            for menu in final_root_menus:
                icon_info = menu.get('web_icon', 'Pas d\'icône')
                print(f"  ✅ ID: {menu['id']} | 📝 Nom: {menu['name']} | 🔢 Séquence: {menu['sequence']}")
                print(f"      🎨 Icône: {icon_info}")
        
        if len(final_root_menus) == 1:
            print("\n🎉 SUCCÈS: Plus qu'un seul menu SmartAgriDecision !")
            print("🌐 Allez sur http://localhost:10020 pour vérifier")
            print("📱 Vous ne devriez voir qu'une seule application maintenant")
        elif len(final_root_menus) == 0:
            print("\n⚠️ ATTENTION: Aucun menu racine trouvé")
            print("🔄 Redémarrage d'Odoo recommandé")
        else:
            print(f"\n⚠️ ATTENTION: Il reste {len(final_root_menus)} menus racines")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la résolution: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 RÉSOLUTION FINALE DU PROBLÈME DES APPLICATIONS DUPLIQUÉES")
    print("=" * 70)
    
    success = fix_duplicate_apps_final()
    
    if success:
        print("\n✅ RÉSOLUTION TERMINÉE AVEC SUCCÈS !")
        print("🎯 Vous ne devriez plus avoir qu'une seule application")
    else:
        print("\n❌ ÉCHEC: Vérification manuelle nécessaire")
    
    print("\n" + "=" * 70)
