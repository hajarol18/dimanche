#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIGRATION SQL DIRECTE
Ajoute directement les colonnes manquantes via PostgreSQL
"""

import psycopg2
import sys

def migration_sql_directe():
    """Migration directe via PostgreSQL"""
    
    print("🔧 MIGRATION SQL DIRECTE - CHAMPS MANQUANTS")
    print("=" * 60)
    
    # Configuration de connexion PostgreSQL
    try:
        print("🔌 Connexion à PostgreSQL...")
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="odoo123",
            user="odoo",
            password="odoo"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("✅ Connecté à PostgreSQL")
        
        # Liste des colonnes à ajouter
        migrations = [
            {
                'table': 'smart_agri_culture',
                'column': 'type_culture',
                'type': 'VARCHAR'
            },
            {
                'table': 'smart_agri_intervention', 
                'column': 'date_prevue',
                'type': 'DATE'
            },
            {
                'table': 'smart_agri_meteostat_import',
                'column': 'statut_import', 
                'type': 'VARCHAR'
            },
            {
                'table': 'smart_agri_alerte_climatique',
                'column': 'severite',
                'type': 'VARCHAR'
            },
            {
                'table': 'smart_agri_ai_model',
                'column': 'statut',
                'type': 'VARCHAR'
            },
            {
                'table': 'smart_agri_ia_predictions',
                'column': 'valeur_predite',
                'type': 'FLOAT'
            }
        ]
        
        print("\n📝 Exécution des migrations SQL...")
        
        for migration in migrations:
            try:
                # Vérifier si la colonne existe déjà
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = %s AND column_name = %s
                """, (migration['table'], migration['column']))
                
                if cursor.fetchone():
                    print(f"✅ Colonne {migration['column']} existe déjà dans {migration['table']}")
                else:
                    # Ajouter la colonne
                    sql = f"ALTER TABLE {migration['table']} ADD COLUMN {migration['column']} {migration['type']}"
                    cursor.execute(sql)
                    print(f"✅ Colonne {migration['column']} ajoutée dans {migration['table']}")
                    
            except Exception as e:
                print(f"⚠️ Erreur {migration['column']} dans {migration['table']}: {str(e)}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 MIGRATION SQL TERMINÉE !")
        print("✅ Toutes les colonnes manquantes ont été ajoutées")
        print("🌐 Vous pouvez maintenant utiliser le module à 100%")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration SQL: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 MIGRATION SQL DIRECTE - CHAMPS MANQUANTS")
    print("=" * 60)
    
    success = migration_sql_directe()
    
    if success:
        print("\n✅ SUCCÈS: Migration SQL terminée avec succès !")
        print("🌐 Allez sur http://localhost:10020 pour vérifier")
    else:
        print("\n❌ ÉCHEC: Problème lors de la migration SQL")
    
    print("\n" + "=" * 60)
