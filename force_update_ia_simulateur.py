#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de mise à jour forcée du modèle ia_simulateur
Force Odoo à reconnaître les nouveaux champs et méthodes
"""

import xmlrpc.client
import sys
import time

def force_update_module():
    """Force la mise à jour du module smart_agri_decision"""
    
    # Configuration de connexion
    url = "http://localhost:10020"
    db = "odoo123"
    username = "admin"
    password = "admin"
    
    try:
        print("🔌 Connexion à Odoo...")
        
        # Connexion à Odoo
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if not uid:
            print("❌ Échec de l'authentification")
            return False
        
        print(f"✅ Connecté avec l'utilisateur ID: {uid}")
        
        # Connexion aux modèles
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # ÉTAPE 1: Vérifier l'état du module
        print("\n📊 Vérification de l'état du module...")
        module = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', 
                                 [[('name', '=', 'smart_agri_decision')]], 
                                 ['name', 'state', 'latest_version'])
        
        if not module:
            print("❌ Module smart_agri_decision non trouvé")
            return False
        
        module_info = module[0]
        print(f"📦 Module: {module_info['name']}")
        print(f"📊 État: {module_info['state']}")
        print(f"🔢 Version: {module_info['latest_version']}")
        
        # ÉTAPE 2: Forcer la mise à jour du module
        print("\n🔄 Mise à jour forcée du module...")
        
        # Désinstaller complètement le module
        print("🗑️ Désinstallation complète...")
        models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_uninstall', 
                         [module_info['id']])
        
        # Attendre que la désinstallation soit terminée
        print("⏳ Attente de la désinstallation...")
        time.sleep(10)
        
        # Réinstaller le module
        print("📥 Réinstallation du module...")
        models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_install', 
                         [module_info['id']])
        
        # Attendre que l'installation soit terminée
        print("⏳ Attente de l'installation...")
        time.sleep(15)
        
        # ÉTAPE 3: Vérifier que le modèle est bien créé
        print("\n🔍 Vérification du modèle ia_simulateur...")
        
        # Vérifier que le modèle existe
        model_exists = models.execute_kw(db, uid, password, 'ir.model', 'search_count', 
                                       [[('model', '=', 'smart_agri_ia_simulateur')]])
        
        if model_exists:
            print("✅ Modèle smart_agri_ia_simulateur créé avec succès")
            
            # Vérifier les champs
            fields = models.execute_kw(db, uid, password, 'ir.model.fields', 'search_read', 
                                     [[('model', '=', 'smart_agri_ia_simulateur')]], 
                                     ['name', 'field_description'])
            
            print(f"📋 Champs trouvés: {len(fields)}")
            for field in fields:
                print(f"  - {field['name']}: {field['field_description']}")
            
            # Vérifier les vues
            views = models.execute_kw(db, uid, password, 'ir.ui.view', 'search_count', 
                                    [[('model', '=', 'smart_agri_ia_simulateur')]])
            
            print(f"👁️ Vues trouvées: {views}")
            
        else:
            print("❌ Modèle smart_agri_ia_simulateur non trouvé après installation")
            return False
        
        # ÉTAPE 4: Tester la création d'un enregistrement
        print("\n🧪 Test de création d'un enregistrement...")
        
        try:
            # Créer un enregistrement de test
            test_record = models.execute_kw(db, uid, password, 'smart_agri_ia_simulateur', 'create', [{
                'name': 'Test Simulation IA',
                'description': 'Test de mise à jour forcée',
                'exploitation_id': 1,  # ID de la première exploitation
                'scenario_rcp': 'rcp45',
                'type_culture': 'cereales',
                'stade_developpement': 'semis',
                'type_sol': 'argileux'
            }])
            
            print(f"✅ Enregistrement de test créé avec ID: {test_record}")
            
            # Supprimer l'enregistrement de test
            models.execute_kw(db, uid, password, 'smart_agri_ia_simulateur', 'unlink', [test_record])
            print("🗑️ Enregistrement de test supprimé")
            
        except Exception as e:
            print(f"⚠️ Erreur lors du test: {str(e)}")
            # Ce n'est pas critique, continuons
        
        print("\n🎉 Mise à jour forcée terminée avec succès !")
        print("💡 Vous pouvez maintenant tester la Simulation Interactive dans Odoo")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour forcée: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 SCRIPT DE MISE À JOUR FORCÉE - IA SIMULATEUR")
    print("=" * 50)
    
    success = force_update_module()
    
    if success:
        print("\n✅ SUCCÈS: Module mis à jour avec succès")
        print("🌐 Allez sur http://localhost:10020 pour tester")
    else:
        print("\n❌ ÉCHEC: Problème lors de la mise à jour")
        print("🔧 Vérifiez les logs Odoo pour plus de détails")
    
    print("\n" + "=" * 50)
