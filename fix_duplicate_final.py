#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT FINAL POUR SUPPRIMER DÉFINITIVEMENT LE MENU DUPLIQUÉ
Supprime le menu ID 282 et ses données XML associées
"""

import xmlrpc.client
import sys
import time

def fix_duplicate_final():
    """Supprime définitivement le menu dupliqué ID 282"""
    
    # Configuration de connexion
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        print("🔧 SUPPRESSION DÉFINITIVE DU MENU DUPLIQUÉ")
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
        
        print("\n🎯 CIBLAGE DU MENU DUPLIQUÉ...")
        
        # Vérifier que le menu ID 282 existe encore
        try:
            menu_282 = models.execute_kw(db, uid, password, 'ir.ui.menu', 'read', [282], ['name', 'web_icon'])
            print(f"📋 Menu ID 282 trouvé: {menu_282['name']}")
            print(f"🎨 Icône: {menu_282.get('web_icon', 'Pas d\'icône')}")
        except Exception as e:
            print(f"⚠️ Menu ID 282 non trouvé: {str(e)}")
            return True
        
        print("\n🗑️ SUPPRESSION DU MENU DUPLIQUÉ...")
        
        # Supprimer le menu ID 282
        try:
            models.execute_kw(db, uid, password, 'ir.ui.menu', 'unlink', [282])
            print("✅ Menu ID 282 supprimé")
        except Exception as e:
            print(f"⚠️ Erreur lors de la suppression du menu: {str(e)}")
        
        print("\n🗑️ SUPPRESSION DES DONNÉES XML ASSOCIÉES...")
        
        # Supprimer les données XML associées au menu dupliqué
        try:
            # Chercher les données XML pour menu_smart_agri_main (ID 282)
            xml_data = models.execute_kw(db, uid, password, 'ir.model.data', 'search', 
                                       [[('model', '=', 'ir.ui.menu'), ('res_id', '=', 282)]])
            
            if xml_data:
                print(f"📄 Données XML trouvées: {xml_data}")
                models.execute_kw(db, uid, password, 'ir.model.data', 'unlink', xml_data)
                print("✅ Données XML supprimées")
            else:
                print("ℹ️ Aucune donnée XML à supprimer")
        except Exception as e:
            print(f"⚠️ Erreur lors de la suppression des données XML: {str(e)}")
        
        # Attendre que les changements prennent effet
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
        else:
            print(f"\n⚠️ ATTENTION: Il reste {len(final_menus)} menus racines")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 SUPPRESSION DÉFINITIVE DU MENU DUPLIQUÉ")
    print("=" * 60)
    
    success = fix_duplicate_final()
    
    if success:
        print("\n✅ SUPPRESSION TERMINÉE AVEC SUCCÈS !")
        print("🎯 Vous ne devriez plus avoir qu'une seule application")
    else:
        print("\n❌ ÉCHEC: Vérification manuelle nécessaire")
    
    print("\n" + "=" * 60)
