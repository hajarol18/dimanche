#!/bin/bash
# Script d'installation automatique pour SmartAgriDecision
# Usage: ./install_dependencies.sh

echo "🌾 Installation des dépendances SmartAgriDecision"
echo "=================================================="

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    echo "Veuillez installer Python 3.8+ d'abord"
    exit 1
fi

echo "✅ Python trouvé: $(python3 --version)"

# Vérifier pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé"
    echo "Veuillez installer pip3 d'abord"
    exit 1
fi

echo "✅ pip trouvé: $(pip3 --version)"

# Créer environnement virtuel
echo "📦 Création de l'environnement virtuel..."
python3 -m venv smartagri_env
source smartagri_env/bin/activate

# Mettre à jour pip
echo "🔄 Mise à jour de pip..."
pip install --upgrade pip

# Installer dépendances minimales
echo "📥 Installation des dépendances minimales..."
pip install -r requirements-minimal.txt

# Installer dépendances complètes (optionnel)
read -p "Voulez-vous installer toutes les dépendances avancées ? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📥 Installation des dépendances complètes..."
    pip install -r addons/smart_agri_decision/requirements.txt
fi

# Vérifier l'installation
echo "🧪 Vérification de l'installation..."
python3 -c "
import pandas as pd
import numpy as np
import sklearn
import psycopg2
import meteostat
print('✅ Toutes les dépendances sont installées correctement!')
"

echo "🎉 Installation terminée!"
echo "Pour activer l'environnement: source smartagri_env/bin/activate"
echo "Pour démarrer Odoo: docker-compose up -d"
