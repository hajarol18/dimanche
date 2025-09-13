#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT POUR RÉSOUDRE LE PROBLÈME DES MULTIPLES APPLICATIONS
Désactive les modules non nécessaires et garde seulement SmartAgriDecision
"""

import xmlrpc.client
import sys
import time

def fix_multiple_apps():
    """Désactive les modules non nécessaires pour garder seulement SmartAgriDecision"""
    
    # Configuration de connexion
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        print("🔧 RÉSOLUTION DU PROBLÈME DES MULTIPLES APPLICATIONS")
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
        
        # Modules à désactiver (garder seulement smart_agri_decision)
        modules_to_disable = [
            'estate',
            'estate1', 
            'gestion_bibliotheque',
            'test_minimal',
            'test_module'
        ]
        
        print("\n📦 VÉRIFICATION DES MODULES INSTALLÉS...")
        
        # Vérifier l'état de tous les modules
        all_modules = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', 
                                      [[('name', 'in', modules_to_disable + ['smart_agri_decision'])]], 
                                      {'fields': ['name', 'state', 'application']})
        
        print("📊 État actuel des modules:")
        for module in all_modules:
            status_icon = "✅" if module['state'] == 'installed' else "❌"
            app_icon = "📱" if module.get('application') else "🔧"
            print(f"  {status_icon} {app_icon} {module['name']}: {module['state']}")
        
        print("\n🚫 DÉSACTIVATION DES MODULES NON NÉCESSAIRES...")
        
        for module_name in modules_to_disable:
            try:
                # Chercher le module
                module = models.execute_kw(db, uid, password, 'ir.module.module', 'search', 
                                         [[('name', '=', module_name)]])
                
                if module:
                    module_id = module[0]
                    
                    # Vérifier s'il est installé
                    module_info = models.execute_kw(db, uid, password, 'ir.module.module', 'read', 
                                                  [module_id], ['state'])
                    
                    if module_info and module_info[0]['state'] == 'installed':
                        print(f"  🔄 Désinstallation de {module_name}...")
                        
                        # Désinstaller le module
                        models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_uninstall', [module_id])
                        print(f"  ✅ {module_name} désinstallé")
                    else:
                        print(f"  ⏭️ {module_name} déjà désinstallé")
                else:
                    print(f"  ⏭️ {module_name} non trouvé")
                    
            except Exception as e:
                print(f"  ⚠️ Erreur avec {module_name}: {str(e)}")
        
        # Attendre un peu pour que les changements prennent effet
        print("\n⏳ Attente de la finalisation des changements...")
        time.sleep(5)
        
        print("\n✅ VÉRIFICATION FINALE...")
        
        # Vérifier l'état final
        final_modules = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', 
                                        [[('name', 'in', modules_to_disable + ['smart_agri_decision'])]], 
                                        {'fields': ['name', 'state', 'application']})
        
        print("📊 État final des modules:")
        for module in final_modules:
            status_icon = "✅" if module['state'] == 'installed' else "❌"
            app_icon = "📱" if module.get('application') else "🔧"
            print(f"  {status_icon} {app_icon} {module['name']}: {module['state']}")
        
        # Vérifier que SmartAgriDecision est toujours actif
        smart_agri = [m for m in final_modules if m['name'] == 'smart_agri_decision']
        if smart_agri and smart_agri[0]['state'] == 'installed':
            print("\n🎉 SUCCÈS: SmartAgriDecision est le seul module actif !")
            print("🌐 Allez sur http://localhost:10020 pour vérifier")
            print("📱 Vous ne devriez voir qu'une seule application maintenant")
        else:
            print("\n⚠️ ATTENTION: SmartAgriDecision n'est pas actif")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la résolution: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 RÉSOLUTION DU PROBLÈME DES MULTIPLES APPLICATIONS")
    print("=" * 60)
    
    success = fix_multiple_apps()
    
    if success:
        print("\n✅ RÉSOLUTION TERMINÉE AVEC SUCCÈS !")
        print("🎯 Vous ne devriez plus avoir qu'une seule application")
    else:
        print("\n❌ ÉCHEC: Vérification manuelle nécessaire")
    
    print("\n" + "=" * 60)
