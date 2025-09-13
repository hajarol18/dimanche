#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour identifier précisément le champ Float avec ondelete
"""

import subprocess
import re

print("🔍 RECHERCHE PRÉCISE DU CHAMP FLOAT ONDELETE")
print("=" * 50)

def run_sql_command(sql):
    """Exécute une commande SQL via Docker"""
    try:
        command = f'docker exec -it odoo-18-docker-compose-master-db-1 psql -U odoo -d odoo123 -c "{sql}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

# 1. Chercher tous les champs Float avec des problèmes
print("\n🔍 Recherche des champs Float problématiques...")

sql_queries = [
    # Chercher dans ir_model_fields
    """
    SELECT 
        f.name as field_name,
        f.model,
        f.ttype,
        f.relation,
        f.ondelete,
        f.selection,
        f.domain
    FROM ir_model_fields f 
    WHERE f.model LIKE '%smart_agri%' 
    AND f.ttype = 'float'
    ORDER BY f.model, f.name;
    """,
    
    # Chercher dans ir_model_data
    """
    SELECT 
        d.name,
        d.model,
        d.res_id,
        d.module
    FROM ir_model_data d 
    WHERE d.model LIKE '%smart_agri%'
    ORDER BY d.model, d.name;
    """,
    
    # Chercher des vues avec ondelete
    """
    SELECT 
        v.name,
        v.model,
        v.type,
        v.arch
    FROM ir_ui_view v 
    WHERE v.model LIKE '%smart_agri%'
    AND v.arch LIKE '%ondelete%'
    ORDER BY v.model, v.name;
    """
]

for i, sql in enumerate(sql_queries, 1):
    print(f"\n📋 Requête {i}:")
    success, stdout, stderr = run_sql_command(sql)
    
    if success:
        print(f"✅ Résultat:")
        print(stdout)
    else:
        print(f"❌ Erreur:")
        print(stderr)

# 2. Chercher spécifiquement les problèmes de sélection
print("\n🔍 Recherche des problèmes de sélection...")

sql_selection = """
SELECT 
    f.name,
    f.model,
    f.ttype,
    f.selection,
    f.ondelete
FROM ir_model_fields f 
WHERE f.model LIKE '%smart_agri%' 
AND f.selection IS NOT NULL
AND f.selection != ''
ORDER BY f.model, f.name;
"""

success, stdout, stderr = run_sql_command(sql_selection)

if success:
    print("✅ Champs avec sélection:")
    print(stdout)
    
    # Analyser les résultats
    lines = stdout.split('\n')
    for line in lines:
        if 'float' in line.lower() and 'ondelete' in line.lower():
            print(f"⚠️ CHAMP PROBLÉMATIQUE DÉTECTÉ: {line}")
else:
    print(f"❌ Erreur: {stderr}")

# 3. Essayer de corriger directement
print("\n🔧 Tentative de correction...")

# Supprimer tous les champs Float avec ondelete
correction_sql = """
UPDATE ir_model_fields 
SET ondelete = NULL 
WHERE model LIKE '%smart_agri%' 
AND ttype = 'float' 
AND ondelete IS NOT NULL;
"""

success, stdout, stderr = run_sql_command(correction_sql)

if success:
    print("✅ Correction appliquée:")
    print(stdout)
else:
    print(f"❌ Erreur correction: {stderr}")

print("\n" + "=" * 50)
print("🎯 RECHERCHE TERMINÉE")
