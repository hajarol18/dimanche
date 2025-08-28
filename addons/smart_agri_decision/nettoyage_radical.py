#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de nettoyage radical des références cachées
"""

import psycopg2
import os
import sys

def nettoyage_radical():
    """Nettoyage radical de toutes les références cachées"""
    
    print("🧹 NETTOYAGE RADICAL DES RÉFÉRENCES CACHÉES...")
    
    try:
        # Connexion à la base de données Odoo
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="odoo18",
            user="odoo",
            password="odoo"
        )
        
        cursor = conn.cursor()
        
        # 1. Suppression des références dans ir_attachment
        print("📁 Nettoyage des fichiers attachés...")
        cursor.execute("""
            DELETE FROM ir_attachment 
            WHERE name LIKE '%demo_data_complet%' 
            OR name LIKE '%demo_data_complet.xml%'
            OR name LIKE '%demo_data_complete%'
            OR name LIKE '%demo_data_final%'
        """)
        print(f"✅ {cursor.rowcount} fichiers attachés supprimés")
        
        # 2. Suppression des références dans ir_model_data
        print("🗃️ Nettoyage des données de modèle...")
        cursor.execute("""
            DELETE FROM ir_model_data 
            WHERE name LIKE '%demo_data_complet%' 
            OR name LIKE '%demo_data_complet.xml%'
            OR name LIKE '%demo_data_complete%'
            OR name LIKE '%demo_data_final%'
        """)
        print(f"✅ {cursor.rowcount} données de modèle supprimées")
        
        # 3. Suppression des références dans ir_module_module
        print("📦 Nettoyage des modules...")
        cursor.execute("""
            UPDATE ir_module_module 
            SET state = 'uninstalled' 
            WHERE name = 'smart_agri_decision'
        """)
        print(f"✅ Module smart_agri_decision marqué comme désinstallé")
        
        # 4. Suppression des références dans ir_ui_view
        print("👁️ Nettoyage des vues...")
        cursor.execute("""
            DELETE FROM ir_ui_view 
            WHERE name LIKE '%demo_data_complet%' 
            OR name LIKE '%demo_data_complete%'
            OR name LIKE '%demo_data_final%'
        """)
        print(f"✅ {cursor.rowcount} vues supprimées")
        
        # 5. Suppression des références dans ir_actions_actions
        print("⚡ Nettoyage des actions...")
        cursor.execute("""
            DELETE FROM ir_actions_actions 
            WHERE name LIKE '%demo_data_complet%' 
            OR name LIKE '%demo_data_complete%'
            OR name LIKE '%demo_data_final%'
        """)
        print(f"✅ {cursor.rowcount} actions supprimées")
        
        # 6. Suppression des références dans ir_ui_menu
        print("🍽️ Nettoyage des menus...")
        cursor.execute("""
            DELETE FROM ir_ui_menu 
            WHERE name LIKE '%demo_data_complet%' 
            OR name LIKE '%demo_data_complete%'
            OR name LIKE '%demo_data_final%'
        """)
        print(f"✅ {cursor.rowcount} menus supprimés")
        
        # 7. Nettoyage des séquences
        print("🔢 Nettoyage des séquences...")
        cursor.execute("""
            DELETE FROM ir_sequence 
            WHERE name LIKE '%demo_data_complet%' 
            OR name LIKE '%demo_data_complete%'
            OR name LIKE '%demo_data_final%'
        """)
        print(f"✅ {cursor.rowcount} séquences supprimées")
        
        # 8. Nettoyage des paramètres système
        print("⚙️ Nettoyage des paramètres...")
        cursor.execute("""
            DELETE FROM ir_config_parameter 
            WHERE key LIKE '%demo_data_complet%' 
            OR key LIKE '%demo_data_complete%'
            OR key LIKE '%demo_data_final%'
        """)
        print(f"✅ {cursor.rowcount} paramètres supprimés")
        
        # 9. Nettoyage des logs
        print("📝 Nettoyage des logs...")
        cursor.execute("""
            DELETE FROM ir_logging 
            WHERE name LIKE '%demo_data_complet%' 
            OR name LIKE '%demo_data_complete%'
            OR name LIKE '%demo_data_final%'
        """)
        print(f"✅ {cursor.rowcount} logs supprimés")
        
        # 10. Nettoyage des sessions
        print("🪑 Nettoyage des sessions...")
        cursor.execute("""
            DELETE FROM ir_session 
            WHERE name LIKE '%demo_data_complet%' 
            OR name LIKE '%demo_data_complete%'
            OR name LIKE '%demo_data_final%'
        """)
        print(f"✅ {cursor.rowcount} sessions supprimées")
        
        # Validation des changements
        conn.commit()
        
        print("\n🎯 NETTOYAGE RADICAL TERMINÉ !")
        print("📋 Récapitulatif des suppressions :")
        print("   - Fichiers attachés")
        print("   - Données de modèle")
        print("   - Vues")
        print("   - Actions")
        print("   - Menus")
        print("   - Séquences")
        print("   - Paramètres")
        print("   - Logs")
        print("   - Sessions")
        
        print("\n🚀 Maintenant tu peux :")
        print("   1. Redémarrer Docker")
        print("   2. Réinstaller le module")
        print("   3. Profiter des données marocaines !")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    nettoyage_radical()
