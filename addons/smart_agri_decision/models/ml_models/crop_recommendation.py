# -*- coding: utf-8 -*-
"""
CropRecommendationModel - Système de recommandation de cultures optimales
Utilise l'IA pour recommander les meilleures cultures selon les conditions
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import joblib
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class CropRecommendationModel:
    """
    Modèle de recommandation de cultures basé sur l'IA
    """
    
    def __init__(self):
        self.model = None
        self.model_type = 'xgboost'  # 'xgboost', 'random_forest', 'gradient_boosting'
        self.label_encoder = LabelEncoder()
        self.encoders = {}  # Pour les variables catégorielles
        self.crop_mapping = {}
        self.feature_importance = None
        self.training_metrics = {}
        self.is_trained = False
        
        # Cultures supportées avec leurs caractéristiques
        self.supported_crops = {
            'ble': {
                'nom': 'Blé',
                'famille': 'cereales',
                'saison': ['automne', 'printemps'],
                'temp_min': 0,
                'temp_max': 35,
                'precip_min': 300,
                'precip_max': 800,
                'ph_min': 6.0,
                'ph_max': 8.0,
                'sol_pref': ['argileux', 'limoneux'],
                'rendement_moyen': 3.5
            },
            'orge': {
                'nom': 'Orge',
                'famille': 'cereales',
                'saison': ['automne', 'printemps'],
                'temp_min': -5,
                'temp_max': 30,
                'precip_min': 250,
                'precip_max': 600,
                'ph_min': 6.0,
                'ph_max': 8.5,
                'sol_pref': ['argileux', 'limoneux', 'sableux'],
                'rendement_moyen': 3.0
            },
            'mais': {
                'nom': 'Maïs',
                'famille': 'cereales',
                'saison': ['printemps', 'ete'],
                'temp_min': 10,
                'temp_max': 40,
                'precip_min': 400,
                'precip_max': 1000,
                'ph_min': 5.5,
                'ph_max': 7.5,
                'sol_pref': ['limoneux', 'argileux'],
                'rendement_moyen': 8.0
            },
            'tournesol': {
                'nom': 'Tournesol',
                'famille': 'oleagineux',
                'saison': ['printemps', 'ete'],
                'temp_min': 8,
                'temp_max': 35,
                'precip_min': 200,
                'precip_max': 600,
                'ph_min': 6.0,
                'ph_max': 8.0,
                'sol_pref': ['limoneux', 'sableux'],
                'rendement_moyen': 2.5
            },
            'pomme_de_terre': {
                'nom': 'Pomme de terre',
                'famille': 'tubercules',
                'saison': ['printemps', 'ete'],
                'temp_min': 5,
                'temp_max': 25,
                'precip_min': 300,
                'precip_max': 700,
                'ph_min': 4.5,
                'ph_max': 6.5,
                'sol_pref': ['limoneux', 'sableux'],
                'rendement_moyen': 25.0
            },
            'tomate': {
                'nom': 'Tomate',
                'famille': 'legumes',
                'saison': ['printemps', 'ete'],
                'temp_min': 15,
                'temp_max': 35,
                'precip_min': 400,
                'precip_max': 800,
                'ph_min': 6.0,
                'ph_max': 7.0,
                'sol_pref': ['limoneux', 'argileux'],
                'rendement_moyen': 40.0
            },
            'olivier': {
                'nom': 'Olivier',
                'famille': 'arboriculture',
                'saison': ['perenne'],
                'temp_min': -5,
                'temp_max': 40,
                'precip_min': 200,
                'precip_max': 600,
                'ph_min': 6.0,
                'ph_max': 8.0,
                'sol_pref': ['limoneux', 'argileux'],
                'rendement_moyen': 15.0
            }
        }
    
    def train(self, X, y, model_type='xgboost', test_size=0.2, random_state=42):
        """
        Entraîne le modèle de recommandation de cultures
        
        Args:
            X: Features (conditions climatiques, sol, contraintes)
            y: Target (cultures optimales)
            model_type: Type de modèle
            test_size: Proportion pour le test
            random_state: Seed pour reproductibilité
        """
        _logger.info(f"Entraînement du modèle de recommandation de cultures ({model_type})...")
        
        self.model_type = model_type
        
        # Encodage des labels
        y_encoded = self.label_encoder.fit_transform(y)
        self.crop_mapping = dict(zip(self.label_encoder.classes_, range(len(self.label_encoder.classes_))))
        
        # Encodage des variables catégorielles dans X
        X_encoded = X.copy()
        for col in X_encoded.select_dtypes(include=['object']).columns:
            if col not in self.encoders:
                le = LabelEncoder()
                X_encoded[col] = le.fit_transform(X_encoded[col].astype(str))
                self.encoders[col] = le
            else:
                X_encoded[col] = self.encoders[col].transform(X_encoded[col].astype(str))
        
        X = X_encoded
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=test_size, random_state=random_state
        )
        
        if model_type == 'xgboost':
            self.model = self._train_xgboost(X_train, y_train, X_test, y_test)
        elif model_type == 'random_forest':
            self.model = self._train_random_forest(X_train, y_train, X_test, y_test)
        elif model_type == 'gradient_boosting':
            self.model = self._train_gradient_boosting(X_train, y_train, X_test, y_test)
        else:
            raise ValueError("Type de modèle non supporté")
        
        # Évaluation
        self._evaluate_model(X_test, y_test)
        
        # Importance des features
        self._calculate_feature_importance()
        
        self.is_trained = True
        _logger.info("Modèle de recommandation entraîné avec succès!")
    
    def _train_xgboost(self, X_train, y_train, X_test, y_test):
        """Entraîne un modèle XGBoost pour la classification"""
        
        params = {
            'n_estimators': 1000,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42,
            'n_jobs': -1,
            'objective': 'multi:softprob',
            'num_class': len(np.unique(y_train))
        }
        
        param_grid = {
            'max_depth': [4, 6, 8],
            'learning_rate': [0.05, 0.1, 0.15],
            'n_estimators': [500, 1000, 1500]
        }
        
        xgb_model = xgb.XGBClassifier(**params)
        
        grid_search = GridSearchCV(
            xgb_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1
        )
        
        grid_search.fit(X_train, y_train)
        
        _logger.info(f"Meilleurs paramètres XGBoost: {grid_search.best_params_}")
        
        return grid_search.best_estimator_
    
    def _train_random_forest(self, X_train, y_train, X_test, y_test):
        """Entraîne un modèle Random Forest"""
        
        params = {
            'n_estimators': 500,
            'max_depth': 10,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'random_state': 42,
            'n_jobs': -1
        }
        
        param_grid = {
            'n_estimators': [200, 500, 1000],
            'max_depth': [8, 10, 12],
            'min_samples_split': [2, 5, 10]
        }
        
        rf_model = RandomForestClassifier(**params)
        
        grid_search = GridSearchCV(
            rf_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1
        )
        
        grid_search.fit(X_train, y_train)
        
        _logger.info(f"Meilleurs paramètres Random Forest: {grid_search.best_params_}")
        
        return grid_search.best_estimator_
    
    def _train_gradient_boosting(self, X_train, y_train, X_test, y_test):
        """Entraîne un modèle Gradient Boosting"""
        
        params = {
            'n_estimators': 500,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'random_state': 42
        }
        
        param_grid = {
            'n_estimators': [200, 500, 1000],
            'max_depth': [4, 6, 8],
            'learning_rate': [0.05, 0.1, 0.15]
        }
        
        gb_model = GradientBoostingClassifier(**params)
        
        grid_search = GridSearchCV(
            gb_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1
        )
        
        grid_search.fit(X_train, y_train)
        
        _logger.info(f"Meilleurs paramètres Gradient Boosting: {grid_search.best_params_}")
        
        return grid_search.best_estimator_
    
    def _evaluate_model(self, X_test, y_test):
        """Évalue les performances du modèle"""
        
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)
        
        # Métriques
        accuracy = accuracy_score(y_test, y_pred)
        
        # Rapport de classification
        class_report = classification_report(
            y_test, y_pred, 
            target_names=self.label_encoder.classes_,
            output_dict=True
        )
        
        self.training_metrics = {
            'accuracy': accuracy,
            'classification_report': class_report
        }
        
        _logger.info(f"Précision du modèle: {accuracy:.3f}")
        _logger.info(f"Rapport de classification:\n{classification_report(y_test, y_pred, target_names=self.label_encoder.classes_)}")
    
    def _calculate_feature_importance(self):
        """Calcule l'importance des features"""
        
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.DataFrame({
                'feature': self.model.feature_names_in_,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
        else:
            self.feature_importance = None
    
    def recommend_crops(self, conditions, top_n=3):
        """
        Recommande les meilleures cultures pour des conditions données
        
        Args:
            conditions: DataFrame avec conditions climatiques et sol
            top_n: Nombre de recommandations à retourner
            
        Returns:
            recommendations: Liste des recommandations avec scores
        """
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant de faire des recommandations")
        
        # Encodage des variables catégorielles pour la prédiction
        conditions_encoded = conditions.copy()
        for col in conditions_encoded.select_dtypes(include=['object']).columns:
            if col in self.encoders:
                conditions_encoded[col] = self.encoders[col].transform(conditions_encoded[col].astype(str))
            else:
                # Si la colonne n'a pas été vue pendant l'entraînement, utiliser une valeur par défaut
                conditions_encoded[col] = 0
        
        # Prédiction des probabilités
        probabilities = self.model.predict_proba(conditions_encoded)
        
        # Classes prédites
        crop_indices = np.argsort(probabilities[0])[::-1][:top_n]
        crop_scores = probabilities[0][crop_indices]
        
        # Conversion en noms de cultures
        crop_names = self.label_encoder.inverse_transform(crop_indices)
        
        recommendations = []
        for i, (crop, score) in enumerate(zip(crop_names, crop_scores)):
            crop_info = self.supported_crops.get(crop, {})
            
            recommendation = {
                'rank': i + 1,
                'crop': crop,
                'crop_name': crop_info.get('nom', crop),
                'confidence_score': float(score),
                'family': crop_info.get('famille', 'unknown'),
                'expected_yield': crop_info.get('rendement_moyen', 0),
                'suitability': self._calculate_suitability(conditions, crop)
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _calculate_suitability(self, conditions, crop):
        """
        Calcule l'adéquation d'une culture aux conditions
        
        Args:
            conditions: Conditions climatiques et sol
            crop: Nom de la culture
            
        Returns:
            suitability: Score d'adéquation (0-100)
        """
        if crop not in self.supported_crops:
            return 50  # Score neutre pour cultures inconnues
        
        crop_info = self.supported_crops[crop]
        suitability_score = 0
        factors = 0
        
        # Vérification température
        if 'temperature_moyenne' in conditions.columns:
            temp = conditions['temperature_moyenne'].iloc[0]
            temp_min = crop_info['temp_min']
            temp_max = crop_info['temp_max']
            
            if temp_min <= temp <= temp_max:
                temp_score = 100
            else:
                temp_score = max(0, 100 - abs(temp - (temp_min + temp_max) / 2) * 5)
            
            suitability_score += temp_score
            factors += 1
        
        # Vérification précipitations
        if 'precipitation_totale' in conditions.columns:
            precip = conditions['precipitation_totale'].iloc[0]
            precip_min = crop_info['precip_min']
            precip_max = crop_info['precip_max']
            
            if precip_min <= precip <= precip_max:
                precip_score = 100
            else:
                precip_score = max(0, 100 - abs(precip - (precip_min + precip_max) / 2) / 10)
            
            suitability_score += precip_score
            factors += 1
        
        # Vérification pH
        if 'ph_sol' in conditions.columns:
            ph = conditions['ph_sol'].iloc[0]
            ph_min = crop_info['ph_min']
            ph_max = crop_info['ph_max']
            
            if ph_min <= ph <= ph_max:
                ph_score = 100
            else:
                ph_score = max(0, 100 - abs(ph - (ph_min + ph_max) / 2) * 20)
            
            suitability_score += ph_score
            factors += 1
        
        # Vérification type de sol
        if 'type_sol' in conditions.columns:
            soil_type = conditions['type_sol'].iloc[0]
            preferred_soils = crop_info['sol_pref']
            
            if soil_type in preferred_soils:
                soil_score = 100
            else:
                soil_score = 50  # Score neutre pour sols non préférés
            
            suitability_score += soil_score
            factors += 1
        
        return suitability_score / factors if factors > 0 else 50
    
    def get_crop_requirements(self, crop):
        """
        Retourne les exigences d'une culture
        
        Args:
            crop: Nom de la culture
            
        Returns:
            dict: Exigences de la culture
        """
        return self.supported_crops.get(crop, {})
    
    def get_all_crops(self):
        """
        Retourne toutes les cultures supportées
        
        Returns:
            dict: Toutes les cultures avec leurs caractéristiques
        """
        return self.supported_crops
    
    def add_custom_crop(self, crop_name, crop_info):
        """
        Ajoute une culture personnalisée
        
        Args:
            crop_name: Nom de la culture
            crop_info: Dictionnaire avec les caractéristiques
        """
        self.supported_crops[crop_name] = crop_info
        _logger.info(f"Culture personnalisée ajoutée: {crop_name}")
    
    def get_feature_importance(self, top_n=10):
        """
        Retourne l'importance des features
        
        Args:
            top_n: Nombre de features à retourner
            
        Returns:
            DataFrame avec les features les plus importantes
        """
        if self.feature_importance is None:
            return None
        
        return self.feature_importance.head(top_n)
    
    def save_model(self, filepath):
        """
        Sauvegarde le modèle entraîné
        
        Args:
            filepath: Chemin de sauvegarde
        """
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant d'être sauvegardé")
        
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'label_encoder': self.label_encoder,
            'crop_mapping': self.crop_mapping,
            'feature_importance': self.feature_importance,
            'training_metrics': self.training_metrics,
            'supported_crops': self.supported_crops,
            'is_trained': self.is_trained,
            'timestamp': datetime.now().isoformat()
        }
        
        joblib.dump(model_data, filepath)
        _logger.info(f"Modèle de recommandation sauvegardé: {filepath}")
    
    def load_model(self, filepath):
        """
        Charge un modèle sauvegardé
        
        Args:
            filepath: Chemin du modèle
        """
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.model_type = model_data['model_type']
        self.label_encoder = model_data['label_encoder']
        self.crop_mapping = model_data['crop_mapping']
        self.feature_importance = model_data['feature_importance']
        self.training_metrics = model_data['training_metrics']
        self.supported_crops = model_data['supported_crops']
        self.is_trained = model_data['is_trained']
        
        _logger.info(f"Modèle de recommandation chargé: {filepath}")
    
    def get_model_info(self):
        """
        Retourne les informations du modèle
        
        Returns:
            dict: Informations du modèle
        """
        return {
            'model_type': self.model_type,
            'is_trained': self.is_trained,
            'supported_crops_count': len(self.supported_crops),
            'training_accuracy': self.training_metrics.get('accuracy', 0),
            'feature_count': len(self.feature_importance) if self.feature_importance is not None else 0,
            'top_features': self.get_feature_importance(5).to_dict('records') if self.feature_importance is not None else []
        }
