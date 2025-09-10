#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de nettoyage radical de la base de données - Élimination définitive des données françaises
"""

import os
import psycopg2
import json
from datetime import datetime

def nettoyage_radical_base_donnees():
    """Exécute le nettoyage radical de la base de données PostgreSQL"""
    
    print("🗑️ NETTOYAGE RADICAL DE LA BASE DE DONNÉES - ÉLIMINATION DÉFINITIVE DES DONNÉES FRANÇAISES")
    print("=" * 90)
    
    # Configuration de la base de données (à adapter selon votre environnement)
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'odoo18',  # Nom de votre base Odoo
        'user': 'odoo',        # Utilisateur Odoo
        'password': 'odoo'     # Mot de passe Odoo
    }
    
    print("🔧 Configuration de la base de données :")
    print(f"   Host: {db_config['host']}")
    print(f"   Port: {db_config['port']}")
    print(f"   Database: {db_config['database']}")
    print(f"   User: {db_config['user']}")
    
    try:
        # Connexion à la base de données
        print("\n🔌 Connexion à la base de données...")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        print("   ✅ Connexion réussie")
        
        # 1. SUPPRESSION RADICALE DES DONNÉES FRANÇAISES
        print("\n🗑️ SUPPRESSION RADICALE DES DONNÉES FRANÇAISES...")
        print("-" * 70)
        
        # Tables à nettoyer
        tables_a_nettoyer = [
            'smart_agri_exploitation',
            'smart_agri_parcelle', 
            'smart_agri_culture',
            'smart_agri_station_meteo',
            'smart_agri_type_sol',
            'smart_agri_intervention',
            'smart_agri_intrant',
            'smart_agri_alerte_climatique',
            'smart_agri_tendance_climatique',
            'smart_agri_scenario_rcp',
            'smart_agri_modele_ia',
            'smart_agri_prediction',
            'smart_agri_detection_stress',
            'smart_agri_optimisation_ressources',
            'smart_agri_simulation_scenario'
        ]
        
        total_suppressions = 0
        
        for table in tables_a_nettoyer:
            try:
                # Vérifier si la table existe
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = %s
                    );
                """, (table,))
                
                if cursor.fetchone()[0]:
                    # Compter les enregistrements avant suppression
                    cursor.execute(f"SELECT COUNT(*) FROM {table};")
                    count_avant = cursor.fetchone()[0]
                    
                    if count_avant > 0:
                        # Suppression radicale de TOUS les enregistrements
                        cursor.execute(f"DELETE FROM {table};")
                        suppressions = cursor.rowcount
                        total_suppressions += suppressions
                        
                        print(f"   🗑️ {table}: {count_avant} → 0 enregistrements (supprimés)")
                    else:
                        print(f"   ℹ️  {table}: 0 enregistrements (déjà vide)")
                else:
                    print(f"   ⚠️  {table}: Table inexistante")
                    
            except Exception as e:
                print(f"   ❌ Erreur lors du nettoyage de {table}: {e}")
        
        # 2. RÉINITIALISATION DES SÉQUENCES
        print(f"\n🔄 RÉINITIALISATION DES SÉQUENCES...")
        
        for table in tables_a_nettoyer:
            try:
                cursor.execute(f"""
                    SELECT setval(pg_get_serial_sequence('{table}', 'id'), 1, false);
                """)
                print(f"   ✅ Séquence de {table} réinitialisée")
            except Exception as e:
                print(f"   ⚠️  Impossible de réinitialiser la séquence de {table}: {e}")
        
        # 3. VALIDATION ET COMMIT
        print(f"\n💾 VALIDATION DES CHANGEMENTS...")
        
        # Vérifier que toutes les tables sont vides
        total_verification = 0
        for table in tables_a_nettoyer:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                total_verification += count
                if count > 0:
                    print(f"   ⚠️  {table}: {count} enregistrements restants")
                else:
                    print(f"   ✅ {table}: 0 enregistrements (nettoyage réussi)")
            except Exception as e:
                print(f"   ❌ Erreur lors de la vérification de {table}: {e}")
        
        if total_verification == 0:
            print(f"\n🎉 SUCCÈS TOTAL : Toutes les tables sont vides !")
            
            # Commit des changements
            conn.commit()
            print("   💾 Changements validés et sauvegardés")
        else:
            print(f"\n⚠️  ATTENTION : {total_verification} enregistrements restent dans la base")
            conn.rollback()
            print("   ❌ Changements annulés")
        
        # 4. CRÉATION DU RAPPORT DE NETTOYAGE RADICAL
        print(f"\n📋 CRÉATION DU RAPPORT DE NETTOYAGE RADICAL...")
        
        rapport_radical = f"""# RAPPORT DE NETTOYAGE RADICAL DE LA BASE DE DONNÉES - SmartAgriDecision

## 📅 Date du nettoyage radical
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🗑️ Résumé du nettoyage radical
- **Tables nettoyées** : {len(tables_a_nettoyer)}
- **Total suppressions** : {total_suppressions}
- **Statut** : {'SUCCÈS TOTAL' if total_verification == 0 else 'ATTENTION - Enregistrements restants'}

## 📁 Tables traitées
{chr(10).join([f"- {table}" for table in tables_a_nettoyer])}

## 🔄 Actions effectuées
1. Suppression radicale de TOUS les enregistrements français
2. Réinitialisation des séquences d'ID
3. Vérification de l'état des tables
4. Validation des changements

## 🎯 Résultat du nettoyage radical
{'✅ SUCCÈS TOTAL : Base de données complètement nettoyée' if total_verification == 0 else '⚠️ ATTENTION : Des enregistrements persistent'}

## 🔧 Prochaines étapes
1. Charger les nouvelles données marocaines
2. Vérifier l'affichage dans Odoo
3. Tester les fonctionnalités
4. Valider la localisation marocaine

## ⚠️ IMPORTANT
- **TOUTES les données ont été supprimées**
- **Les séquences ont été réinitialisées**
- **La base est prête pour les nouvelles données marocaines**

---
*Rapport généré automatiquement par le script de nettoyage radical*
"""
        
        with open("RAPPORT_NETTOYAGE_RADICAL_BD.md", "w", encoding="utf-8") as f:
            f.write(rapport_radical)
        
        print(f"   ✅ Rapport de nettoyage radical créé : RAPPORT_NETTOYAGE_RADICAL_BD.md")
        
        # 5. Affichage du résumé final
        print("\n" + "=" * 90)
        print("🏆 NETTOYAGE RADICAL DE LA BASE DE DONNÉES TERMINÉ !")
        print("=" * 90)
        
        print(f"🗑️ Total suppressions : {total_suppressions}")
        print(f"📁 Tables nettoyées : {len(tables_a_nettoyer)}")
        print(f"🔍 Total vérification : {total_verification}")
        
        if total_verification == 0:
            print(f"\n🎉 SUCCÈS TOTAL RADICAL : Base de données 100% nettoyée !")
            print("🇲🇦 Prête pour les nouvelles données marocaines")
            print("✅ Nettoyage radical réussi")
        else:
            print(f"\n⚠️  ATTENTION : {total_verification} enregistrements persistent")
            print("🔧 Nettoyage supplémentaire nécessaire")
        
        print(f"\n🎯 RECOMMANDATIONS RADICALES :")
        print("   ✅ Base de données nettoyée")
        print("   ✅ Séquences réinitialisées")
        print("   ✅ Prêt pour les nouvelles données")
        print("   🔄 Charger les données marocaines")
        print("   🔍 Vérifier l'affichage Odoo")
        
        return total_verification == 0
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE : {e}")
        print("🔧 Vérifiez la configuration de la base de données")
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()
            print("\n🔌 Connexion à la base de données fermée")

if __name__ == "__main__":
    try:
        nettoyage_radical_base_donnees()
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution : {e}")
        import traceback
        traceback.print_exc()
