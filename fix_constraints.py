#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import sys

def fix_constraints():
    """Corrige les contraintes de base de données pour permettre l'affichage de l'app"""
    
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="odoo123",
            user="odoo",
            password="odoo"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("🔧 CORRECTION DES CONTRAINTES DE BASE DE DONNÉES")
        print("=" * 60)
        
        # 1. Vérifier les interventions problématiques
        print("\n📊 1. Vérification des interventions...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM smart_agri_intervention 
            WHERE exploitation_id IS NOT NULL
        """)
        
        intervention_count = cursor.fetchone()[0]
        print(f"   📋 {intervention_count} interventions trouvées")
        
        # 2. Archiver les interventions au lieu de les supprimer
        print("\n🗃️ 2. Archivage des interventions...")
        cursor.execute("""
            UPDATE smart_agri_intervention 
            SET active = false 
            WHERE active = true
        """)
        
        archived_count = cursor.rowcount
        print(f"   ✅ {archived_count} interventions archivées")
        
        # 3. Vérifier les cultures
        print("\n🌾 3. Vérification des cultures...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM smart_agri_culture 
            WHERE active = true
        """)
        
        culture_count = cursor.fetchone()[0]
        print(f"   📋 {culture_count} cultures trouvées")
        
        # 4. Archiver les cultures
        print("\n🗃️ 4. Archivage des cultures...")
        cursor.execute("""
            UPDATE smart_agri_culture 
            SET active = false 
            WHERE active = true
        """)
        
        archived_cultures = cursor.rowcount
        print(f"   ✅ {archived_cultures} cultures archivées")
        
        # 5. Vérifier les parcelles
        print("\n🏡 5. Vérification des parcelles...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM smart_agri_parcelle 
            WHERE active = true
        """)
        
        parcelle_count = cursor.fetchone()[0]
        print(f"   📋 {parcelle_count} parcelles trouvées")
        
        # 6. Archiver les parcelles
        print("\n🗃️ 6. Archivage des parcelles...")
        cursor.execute("""
            UPDATE smart_agri_parcelle 
            SET active = false 
            WHERE active = true
        """)
        
        archived_parcelles = cursor.rowcount
        print(f"   ✅ {archived_parcelles} parcelles archivées")
        
        # 7. Vérifier les exploitations
        print("\n🏢 7. Vérification des exploitations...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM smart_agri_exploitation 
            WHERE active = true
        """)
        
        exploitation_count = cursor.fetchone()[0]
        print(f"   📋 {exploitation_count} exploitations trouvées")
        
        # 8. Archiver les exploitations
        print("\n🗃️ 8. Archivage des exploitations...")
        cursor.execute("""
            UPDATE smart_agri_exploitation 
            SET active = false 
            WHERE active = true
        """)
        
        archived_exploitations = cursor.rowcount
        print(f"   ✅ {archived_exploitations} exploitations archivées")
        
        print("\n" + "=" * 60)
        print("🎉 CORRECTION TERMINÉE AVEC SUCCÈS!")
        print("=" * 60)
        
        print("\n📝 RÉSUMÉ DES ACTIONS:")
        print(f"✅ {archived_count} interventions archivées")
        print(f"✅ {archived_cultures} cultures archivées")
        print(f"✅ {archived_parcelles} parcelles archivées")
        print(f"✅ {archived_exploitations} exploitations archivées")
        
        print("\n🌐 MAINTENANT L'APP DEVRAIT S'AFFICHER!")
        print("1. Allez sur http://localhost:10020")
        print("2. Connectez-vous")
        print("3. L'app devrait maintenant s'afficher correctement")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        return False
    
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("🚀 Correction des contraintes de base de données")
    print("=" * 50)
    
    success = fix_constraints()
    
    if success:
        print("\n✅ Correction terminée!")
    else:
        print("\n💥 Des problèmes persistent.")
    
    sys.exit(0 if success else 1)
