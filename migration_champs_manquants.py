#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIGRATION POUR AJOUTER LES CHAMPS MANQUANTS
Ajoute les champs calculés manquants dans la base de données
"""

import xmlrpc.client
import psycopg2
from datetime import datetime

def migration_champs_manquants():
    """Migration pour ajouter les champs manquants"""
    
    url = "http://localhost:10020"
    db = "odoo123"
    username = "hajar"
    password = "hajar"
    
    try:
        print("🔧 MIGRATION: AJOUT DES CHAMPS MANQUANTS")
        print("=" * 50)
        print("🎯 Ajout des champs calculés dans la base de données")
        print("=" * 50)
        
        # Connexion directe à PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="odoo",
            password="odoo"
        )
        cur = conn.cursor()
        
        print("✅ Connecté à PostgreSQL")
        
        # 1. Ajouter les champs manquants dans smart_agri_exploitation
        print("\n🏡 Ajout des champs dans smart_agri_exploitation...")
        
        champs_exploitation = [
            "ALTER TABLE smart_agri_exploitation ADD COLUMN IF NOT EXISTS nombre_parcelles INTEGER DEFAULT 0;",
            "ALTER TABLE smart_agri_exploitation ADD COLUMN IF NOT EXISTS surface_utilisee FLOAT DEFAULT 0.0;",
            "ALTER TABLE smart_agri_exploitation ADD COLUMN IF NOT EXISTS surface_disponible FLOAT DEFAULT 0.0;",
            "ALTER TABLE smart_agri_exploitation ADD COLUMN IF NOT EXISTS surface_totale FLOAT DEFAULT 0.0;"
        ]
        
        for champ in champs_exploitation:
            try:
                cur.execute(champ)
                print(f"  ✅ {champ.split('ADD COLUMN IF NOT EXISTS')[1].split(' ')[1]}")
            except Exception as e:
                print(f"  ⚠️ Erreur: {str(e)}")
        
        # 2. Ajouter les champs manquants dans smart_agri_parcelle
        print("\n🗺️ Ajout des champs dans smart_agri_parcelle...")
        
        champs_parcelle = [
            "ALTER TABLE smart_agri_parcelle ADD COLUMN IF NOT EXISTS surface_utilisee FLOAT DEFAULT 0.0;",
            "ALTER TABLE smart_agri_parcelle ADD COLUMN IF NOT EXISTS culture_active_id INTEGER;",
            "ALTER TABLE smart_agri_parcelle ADD COLUMN IF NOT EXISTS nombre_interventions INTEGER DEFAULT 0;"
        ]
        
        for champ in champs_parcelle:
            try:
                cur.execute(champ)
                print(f"  ✅ {champ.split('ADD COLUMN IF NOT EXISTS')[1].split(' ')[1]}")
            except Exception as e:
                print(f"  ⚠️ Erreur: {str(e)}")
        
        # 3. Ajouter les champs manquants dans smart_agri_culture
        print("\n🌾 Ajout des champs dans smart_agri_culture...")
        
        champs_culture = [
            "ALTER TABLE smart_agri_culture ADD COLUMN IF NOT EXISTS duree_culture INTEGER DEFAULT 0;",
            "ALTER TABLE smart_agri_culture ADD COLUMN IF NOT EXISTS rendement_total FLOAT DEFAULT 0.0;",
            "ALTER TABLE smart_agri_culture ADD COLUMN IF NOT EXISTS nombre_interventions INTEGER DEFAULT 0;"
        ]
        
        for champ in champs_culture:
            try:
                cur.execute(champ)
                print(f"  ✅ {champ.split('ADD COLUMN IF NOT EXISTS')[1].split(' ')[1]}")
            except Exception as e:
                print(f"  ⚠️ Erreur: {str(e)}")
        
        # 4. Mettre à jour les valeurs par défaut
        print("\n📊 Mise à jour des valeurs par défaut...")
        
        # Mettre à jour surface_totale = superficie_totale
        cur.execute("UPDATE smart_agri_exploitation SET surface_totale = superficie_totale WHERE superficie_totale IS NOT NULL;")
        print("  ✅ surface_totale mis à jour")
        
        # Mettre à jour surface_utilisee = surface pour les parcelles
        cur.execute("UPDATE smart_agri_parcelle SET surface_utilisee = surface WHERE surface IS NOT NULL;")
        print("  ✅ surface_utilisee mis à jour pour les parcelles")
        
        # Calculer surface_utilisee pour les exploitations
        cur.execute("""
            UPDATE smart_agri_exploitation 
            SET surface_utilisee = (
                SELECT COALESCE(SUM(surface), 0) 
                FROM smart_agri_parcelle 
                WHERE exploitation_id = smart_agri_exploitation.id
            );
        """)
        print("  ✅ surface_utilisee calculé pour les exploitations")
        
        # Calculer nombre_parcelles pour les exploitations
        cur.execute("""
            UPDATE smart_agri_exploitation 
            SET nombre_parcelles = (
                SELECT COUNT(*) 
                FROM smart_agri_parcelle 
                WHERE exploitation_id = smart_agri_exploitation.id
            );
        """)
        print("  ✅ nombre_parcelles calculé pour les exploitations")
        
        # Calculer surface_disponible
        cur.execute("""
            UPDATE smart_agri_exploitation 
            SET surface_disponible = COALESCE(surface_totale, 0) - COALESCE(surface_utilisee, 0);
        """)
        print("  ✅ surface_disponible calculé")
        
        # Valider les changements
        conn.commit()
        print("\n✅ Migration terminée avec succès !")
        
        # Fermer la connexion
        cur.close()
        conn.close()
        
        # 5. Tester la connexion Odoo
        print("\n🧪 Test de la connexion Odoo...")
        
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # Tester la lecture des champs calculés
        exploitations = models.execute_kw(db, uid, password, 'smart_agri_exploitation', 'search_read', 
                                        [[]], {'fields': ['name', 'nombre_parcelles', 'surface_utilisee', 'surface_disponible']})
        
        print(f"  ✅ {len(exploitations)} exploitations lues avec succès")
        for exp in exploitations[:3]:  # Afficher les 3 premières
            print(f"    - {exp['name']}: {exp.get('nombre_parcelles', 0)} parcelles, {exp.get('surface_utilisee', 0)} ha utilisés")
        
        print(f"\n🎉 MIGRATION RÉUSSIE !")
        print(f"📋 Tous les champs calculés sont maintenant disponibles")
        print(f"🚀 Vous pouvez maintenant créer des parcelles et cultures")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {str(e)}")
        return False

if __name__ == "__main__":
    migration_champs_manquants()