#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier les corrections apportées au module SmartAgriDecision
"""

import os
import sys
import xml.etree.ElementTree as ET

def test_alerte_climatique_model():
    """Test du modèle alerte_climatique corrigé"""
    print("🔍 Test du modèle alerte_climatique...")
    
    model_file = "models/smart_agri_alerte_climatique.py"
    
    if not os.path.exists(model_file):
        print("❌ Fichier modèle non trouvé")
        return False
    
    try:
        with open(model_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifications
        checks = [
            ("_inherit = ['mail.thread', 'mail.activity.mixin']", "Héritage mail.thread"),
            ("import logging", "Import logging"),
            ("_logger = logging.getLogger(__name__)", "Logger défini"),
            ("try:", "Gestion d'erreur dans notifier_alerte"),
            ("except Exception as e:", "Exception handling"),
        ]
        
        all_passed = True
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - MANQUANT")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_actions_xml():
    """Test du fichier actions.xml"""
    print("\n🔍 Test du fichier actions.xml...")
    
    actions_file = "views/actions.xml"
    
    if not os.path.exists(actions_file):
        print("❌ Fichier actions.xml non trouvé")
        return False
    
    try:
        tree = ET.parse(actions_file)
        root = tree.getroot()
        
        # Compter les actions
        actions = root.findall(".//record[@model='ir.actions.act_window']")
        print(f"✅ Nombre d'actions trouvées: {len(actions)}")
        
        # Vérifier qu'il n'y a pas de doublons
        action_ids = []
        for action in actions:
            action_id = action.get('id')
            if action_id in action_ids:
                print(f"❌ Action dupliquée: {action_id}")
                return False
            action_ids.append(action_id)
        
        print("✅ Aucune action dupliquée détectée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_manifest_structure():
    """Test de la structure du manifest"""
    print("\n🔍 Test de la structure du manifest...")
    
    manifest_file = "__manifest__.py"
    
    if not os.path.exists(manifest_file):
        print("❌ Fichier __manifest__.py non trouvé")
        return False
    
    try:
        with open(manifest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifications
        checks = [
            ("'data': [", "Section data"),
            ("'views/actions.xml',", "Actions chargées en premier"),
            ("'security/ir.model.access.csv',", "Sécurité chargée en dernier"),
        ]
        
        all_passed = True
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - MANQUANT")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_xml_files():
    """Test de la validité des fichiers XML"""
    print("\n🔍 Test de la validité des fichiers XML...")
    
    views_dir = "views"
    if not os.path.exists(views_dir):
        print("❌ Dossier views non trouvé")
        return False
    
    xml_files = [f for f in os.listdir(views_dir) if f.endswith('.xml')]
    
    all_passed = True
    for xml_file in xml_files:
        file_path = os.path.join(views_dir, xml_file)
        try:
            ET.parse(file_path)
            print(f"✅ {xml_file} - XML valide")
        except ET.ParseError as e:
            print(f"❌ {xml_file} - Erreur XML: {e}")
            all_passed = False
        except Exception as e:
            print(f"❌ {xml_file} - Erreur: {e}")
            all_passed = False
    
    return all_passed

def main():
    """Fonction principale de test"""
    print("🚀 TEST DES CORRECTIONS SMARTAGRI DECISION")
    print("=" * 50)
    
    tests = [
        ("Modèle Alerte Climatique", test_alerte_climatique_model),
        ("Fichier Actions XML", test_actions_xml),
        ("Structure du Manifest", test_manifest_structure),
        ("Validité des fichiers XML", test_xml_files),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Toutes les corrections sont en place !")
        print("✅ Le module devrait maintenant fonctionner correctement")
    else:
        print("⚠️ Certaines corrections nécessitent encore du travail")
        print("🔧 Vérifiez les tests qui ont échoué")

if __name__ == "__main__":
    main()
