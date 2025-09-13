# -*- coding: utf-8 -*-
"""
DataPreprocessor - Préprocesseur de données pour SmartAgriDecision
Gère la préparation des données pour les modèles ML
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import logging

_logger = logging.getLogger(__name__)

class DataPreprocessor:
    """
    Classe pour le préprocessing des données agricoles
    """
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
        self.feature_columns = []
        
    def prepare_yield_data(self, data):
        """
        Prépare les données pour la prédiction de rendement
        
        Args:
            data: DataFrame avec colonnes météo, sol, culture
            
        Returns:
            X, y: Features et target préparés
        """
        _logger.info("Préparation des données de rendement...")
        
        # Sélection des features
        feature_cols = [
            'temperature_moyenne', 'precipitation_totale', 'humidite_relative',
            'rayonnement_solaire', 'ph_sol', 'materiel_organique',
            'type_culture', 'stade_developpement', 'surface_parcelle',
            'densite_semis', 'type_sol', 'pente', 'altitude'
        ]
        
        # Filtrage des colonnes disponibles
        available_cols = [col for col in feature_cols if col in data.columns]
        X = data[available_cols].copy()
        y = data['rendement_observe'] if 'rendement_observe' in data.columns else None
        
        # Gestion des valeurs manquantes
        X = self._handle_missing_values(X)
        
        # Encodage des variables catégorielles
        X = self._encode_categorical_features(X)
        
        # Normalisation des features numériques
        X = self._normalize_numerical_features(X)
        
        self.feature_columns = X.columns.tolist()
        
        return X, y
    
    def prepare_crop_recommendation_data(self, data):
        """
        Prépare les données pour la recommandation de culture
        
        Args:
            data: DataFrame avec conditions climatiques et sol
            
        Returns:
            X, y: Features et cultures recommandées
        """
        _logger.info("Préparation des données de recommandation...")
        
        feature_cols = [
            'temperature_moyenne', 'precipitation_totale', 'humidite_relative',
            'ph_sol', 'materiel_organique', 'type_sol', 'pente', 'altitude',
            'saison', 'region', 'contraintes_budget', 'contraintes_eau'
        ]
        
        available_cols = [col for col in feature_cols if col in data.columns]
        X = data[available_cols].copy()
        y = data['culture_optimale'] if 'culture_optimale' in data.columns else None
        
        X = self._handle_missing_values(X)
        X = self._encode_categorical_features(X)
        X = self._normalize_numerical_features(X)
        
        return X, y
    
    def prepare_stress_detection_data(self, data):
        """
        Prépare les données pour la détection de stress
        
        Args:
            data: DataFrame avec données météo temps réel et état des cultures
            
        Returns:
            X, y: Features et types de stress
        """
        _logger.info("Préparation des données de détection de stress...")
        
        feature_cols = [
            'temperature_actuelle', 'precipitation_7j', 'humidite_sol',
            'indice_vegetation', 'stress_hydrique_historique',
            'temperature_max_7j', 'precipitation_manquante',
            'stade_culture', 'type_culture'
        ]
        
        available_cols = [col for col in feature_cols if col in data.columns]
        X = data[available_cols].copy()
        y = data['type_stress'] if 'type_stress' in data.columns else None
        
        X = self._handle_missing_values(X)
        X = self._encode_categorical_features(X)
        X = self._normalize_numerical_features(X)
        
        return X, y
    
    def prepare_rcp_scenario_data(self, data, rcp_scenario='rcp45'):
        """
        Prépare les données pour les scénarios RCP
        
        Args:
            data: DataFrame de base
            rcp_scenario: Scénario RCP ('rcp45', 'rcp85')
            
        Returns:
            X: Features avec projections climatiques
        """
        _logger.info(f"Préparation des données RCP {rcp_scenario}...")
        
        # Ajout des projections climatiques selon le scénario
        if rcp_scenario == 'rcp45':
            data['temperature_proj'] = data['temperature_moyenne'] + 2.5
            data['precipitation_proj'] = data['precipitation_totale'] * 0.85
        elif rcp_scenario == 'rcp85':
            data['temperature_proj'] = data['temperature_moyenne'] + 4.5
            data['precipitation_proj'] = data['precipitation_totale'] * 0.70
        
        # Features pour simulation
        feature_cols = [
            'temperature_proj', 'precipitation_proj', 'ph_sol',
            'materiel_organique', 'type_sol', 'altitude'
        ]
        
        available_cols = [col for col in feature_cols if col in data.columns]
        X = data[available_cols].copy()
        
        X = self._handle_missing_values(X)
        X = self._encode_categorical_features(X)
        X = self._normalize_numerical_features(X)
        
        return X
    
    def _handle_missing_values(self, X):
        """Gère les valeurs manquantes"""
        for col in X.select_dtypes(include=[np.number]).columns:
            if X[col].isnull().any():
                imputer = SimpleImputer(strategy='median')
                X[col] = imputer.fit_transform(X[[col]]).ravel()
                self.imputers[col] = imputer
        
        for col in X.select_dtypes(include=['object']).columns:
            if X[col].isnull().any():
                X[col] = X[col].fillna('Unknown')
        
        return X
    
    def _encode_categorical_features(self, X):
        """Encode les variables catégorielles"""
        for col in X.select_dtypes(include=['object']).columns:
            if col not in self.encoders:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                self.encoders[col] = le
            else:
                X[col] = self.encoders[col].transform(X[col].astype(str))
        
        return X
    
    def _normalize_numerical_features(self, X):
        """Normalise les features numériques"""
        numerical_cols = X.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if col not in self.scalers:
                scaler = StandardScaler()
                X[col] = scaler.fit_transform(X[[col]]).ravel()
                self.scalers[col] = scaler
            else:
                X[col] = self.scalers[col].transform(X[[col]]).ravel()
        
        return X
    
    def create_weather_features(self, weather_data):
        """
        Crée des features météo avancées
        
        Args:
            weather_data: DataFrame avec données météo brutes
            
        Returns:
            DataFrame avec features météo enrichies
        """
        df = weather_data.copy()
        
        # Moyennes mobiles
        df['temp_moy_7j'] = df['temperature'].rolling(window=7).mean()
        df['precip_moy_30j'] = df['precipitation'].rolling(window=30).mean()
        
        # Indices de stress
        df['stress_thermique'] = np.where(df['temperature'] > 35, 1, 0)
        df['stress_hydrique'] = np.where(df['precipitation'] < 5, 1, 0)
        
        # Saisons
        df['mois'] = pd.to_datetime(df['date']).dt.month
        df['saison'] = df['mois'].map({
            12: 'hiver', 1: 'hiver', 2: 'hiver',
            3: 'printemps', 4: 'printemps', 5: 'printemps',
            6: 'ete', 7: 'ete', 8: 'ete',
            9: 'automne', 10: 'automne', 11: 'automne'
        })
        
        return df
    
    def create_soil_features(self, soil_data):
        """
        Crée des features de sol avancées
        
        Args:
            soil_data: DataFrame avec données de sol
            
        Returns:
            DataFrame avec features de sol enrichies
        """
        df = soil_data.copy()
        
        # Indice de fertilité
        df['indice_fertilite'] = (
            df['ph_sol'] * 0.3 + 
            df['materiel_organique'] * 0.4 + 
            df['azote'] * 0.3
        )
        
        # Capacité de rétention d'eau
        df['capacite_retention'] = (
            df['argile'] * 0.4 + 
            df['limon'] * 0.3 + 
            df['sable'] * 0.1
        )
        
        return df
