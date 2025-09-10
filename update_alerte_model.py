#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de mise à jour du modèle smart_agri_alerte_climatique
Ajoute les nouveaux champs pour la logique intelligente
"""

import psycopg2
import sys
from datetime import datetime

def update_alerte_model():
    """Met à jour le modèle d'alerte climatique"""
    
    # Configuration de connexion
    DB_CONFIG = {
        'host': 'localhost',
        'port': 5432,
        'database': 'odoo',
        'user': 'odoo',
        'password': 'odoo'
    }
    
    try:
        # Connexion à la base de données
        print("🔌 Connexion à la base de données PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("✅ Connexion réussie !")
        
        # Vérifier si les champs existent déjà
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'smart_agri_alerte_climatique' 
            AND column_name IN ('valeur_detectee', 'seuil_alerte', 'type_source')
        """)
        
        existing_fields = [row[0] for row in cursor.fetchall()]
        print(f"📋 Champs existants: {existing_fields}")
        
        # Ajouter les champs manquants
        fields_to_add = []
        
        if 'valeur_detectee' not in existing_fields:
            fields_to_add.append("ADD COLUMN valeur_detectee NUMERIC")
            
        if 'seuil_alerte' not in existing_fields:
            fields_to_add.append("ADD COLUMN seuil_alerte NUMERIC")
            
        if 'type_source' not in existing_fields:
            fields_to_add.append("ADD COLUMN type_source VARCHAR(50)")
        
        if fields_to_add:
            print(f"🔧 Ajout de {len(fields_to_add)} champs...")
            
            # Ajouter les champs un par un
            for field_sql in fields_to_add:
                try:
                    sql = f"ALTER TABLE smart_agri_alerte_climatique {field_sql}"
                    print(f"   Exécution: {sql}")
                    cursor.execute(sql)
                    print(f"   ✅ Champ ajouté avec succès")
                except Exception as e:
                    print(f"   ❌ Erreur: {e}")
            
            # Mettre à jour les vues système Odoo
            print("🔄 Mise à jour des vues système Odoo...")
            
            # Mettre à jour ir.model.fields
            cursor.execute("""
                INSERT INTO ir_model_fields (name, model, field_description, ttype, required, readonly, 
                                          selectable, translate, help, state, modules)
                VALUES 
                ('valeur_detectee', 'smart_agri_alerte_climatique', 'Valeur détectée', 'float', false, false, true, false, 'Valeur qui a déclenché l''alerte', 'manual', 'smart_agri_decision'),
                ('seuil_alerte', 'smart_agri_alerte_climatique', 'Seuil d''alerte', 'float', false, false, true, false, 'Seuil à partir duquel l''alerte se déclenche', 'manual', 'smart_agri_decision'),
                ('type_source', 'smart_agri_alerte_climatique', 'Type de source', 'selection', false, false, true, false, 'Type de source de l''alerte', 'manual', 'smart_agri_decision')
                ON CONFLICT (model, name) DO NOTHING
            """)
            
            print("✅ Champs système ajoutés")
            
            # Commit des changements
            conn.commit()
            print("💾 Changements sauvegardés dans la base de données")
            
        else:
            print("✅ Tous les champs sont déjà présents !")
        
        # Vérifier la structure finale
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'smart_agri_alerte_climatique' 
            AND column_name IN ('valeur_detectee', 'seuil_alerte', 'type_source')
            ORDER BY column_name
        """)
        
        print("\n📊 Structure finale des nouveaux champs:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]} (nullable: {row[2]})")
        
        print("\n🎉 Mise à jour terminée avec succès !")
        print("💡 Vous pouvez maintenant mettre à jour le module smart_agri_decision")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        if 'conn' in locals():
            conn.rollback()
        sys.exit(1)
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            print("🔌 Connexion fermée")

if __name__ == "__main__":
    print("🚀 Script de mise à jour du modèle d'alerte climatique")
    print("=" * 60)
    update_alerte_model()
