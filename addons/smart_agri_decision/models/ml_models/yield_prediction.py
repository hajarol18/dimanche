# -*- coding: utf-8 -*-
"""
YieldPredictionModel - Modèle de prédiction de rendement
Utilise XGBoost et Random Forest pour prédire les rendements agricoles
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import joblib
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class YieldPredictionModel:
    """
    Modèle de prédiction de rendement basé sur l'IA
    """
    
    def __init__(self):
        self.model = None
        self.model_type = 'xgboost'  # 'xgboost' ou 'random_forest'
        self.feature_importance = None
        self.training_metrics = {}
        self.is_trained = False
        
    def train(self, X, y, model_type='xgboost', test_size=0.2, random_state=42):
        """
        Entraîne le modèle de prédiction de rendement
        
        Args:
            X: Features (météo, sol, culture)
            y: Target (rendement observé)
            model_type: Type de modèle ('xgboost' ou 'random_forest')
            test_size: Proportion pour le test
            random_state: Seed pour reproductibilité
        """
        _logger.info(f"Entraînement du modèle de prédiction de rendement ({model_type})...")
        
        self.model_type = model_type
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        if model_type == 'xgboost':
            self.model = self._train_xgboost(X_train, y_train, X_test, y_test)
        elif model_type == 'random_forest':
            self.model = self._train_random_forest(X_train, y_train, X_test, y_test)
        else:
            raise ValueError("Type de modèle non supporté. Utilisez 'xgboost' ou 'random_forest'")
        
        # Évaluation
        self._evaluate_model(X_test, y_test)
        
        # Importance des features
        self._calculate_feature_importance()
        
        self.is_trained = True
        _logger.info("Modèle entraîné avec succès!")
        
    def _train_xgboost(self, X_train, y_train, X_test, y_test):
        """Entraîne un modèle XGBoost"""
        
        # Paramètres optimaux pour l'agriculture
        params = {
            'n_estimators': 1000,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42,
            'n_jobs': -1
        }
        
        # Grid search pour optimisation
        param_grid = {
            'max_depth': [4, 6, 8],
            'learning_rate': [0.05, 0.1, 0.15],
            'n_estimators': [500, 1000, 1500]
        }
        
        xgb_model = xgb.XGBRegressor(**params)
        
        # Recherche des meilleurs paramètres
        grid_search = GridSearchCV(
            xgb_model, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1
        )
        
        grid_search.fit(X_train, y_train)
        
        _logger.info(f"Meilleurs paramètres XGBoost: {grid_search.best_params_}")
        
        return grid_search.best_estimator_
    
    def _train_random_forest(self, X_train, y_train, X_test, y_test):
        """Entraîne un modèle Random Forest"""
        
        # Paramètres optimaux
        params = {
            'n_estimators': 500,
            'max_depth': 10,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'random_state': 42,
            'n_jobs': -1
        }
        
        # Grid search
        param_grid = {
            'n_estimators': [200, 500, 1000],
            'max_depth': [8, 10, 12],
            'min_samples_split': [2, 5, 10]
        }
        
        rf_model = RandomForestRegressor(**params)
        
        grid_search = GridSearchCV(
            rf_model, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1
        )
        
        grid_search.fit(X_train, y_train)
        
        _logger.info(f"Meilleurs paramètres Random Forest: {grid_search.best_params_}")
        
        return grid_search.best_estimator_
    
    def _evaluate_model(self, X_test, y_test):
        """Évalue les performances du modèle"""
        
        y_pred = self.model.predict(X_test)
        
        # Métriques
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        
        self.training_metrics = {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
            'mape': mape
        }
        
        _logger.info(f"Performance du modèle:")
        _logger.info(f"  RMSE: {rmse:.2f} t/ha")
        _logger.info(f"  MAE: {mae:.2f} t/ha")
        _logger.info(f"  R²: {r2:.3f}")
        _logger.info(f"  MAPE: {mape:.1f}%")
    
    def _calculate_feature_importance(self):
        """Calcule l'importance des features"""
        
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.DataFrame({
                'feature': self.model.feature_names_in_,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
        else:
            self.feature_importance = None
    
    def predict(self, X):
        """
        Prédit le rendement pour de nouvelles données
        
        Args:
            X: Features (météo, sol, culture)
            
        Returns:
            predictions: Prédictions de rendement
        """
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant de faire des prédictions")
        
        predictions = self.model.predict(X)
        return predictions
    
    def predict_with_confidence(self, X):
        """
        Prédit le rendement avec intervalle de confiance
        
        Args:
            X: Features
            
        Returns:
            predictions, confidence_interval: Prédictions et intervalles
        """
        predictions = self.predict(X)
        
        # Calcul de l'intervalle de confiance (approximation)
        if hasattr(self.model, 'estimators_'):
            # Pour Random Forest, on peut calculer la variance
            individual_predictions = np.array([
                tree.predict(X) for tree in self.model.estimators_
            ])
            std = np.std(individual_predictions, axis=0)
            confidence_interval = 1.96 * std  # 95% de confiance
        else:
            # Pour XGBoost, approximation basée sur l'erreur d'entraînement
            confidence_interval = np.full(len(predictions), self.training_metrics.get('rmse', 1.0))
        
        return predictions, confidence_interval
    
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
    
    def explain_prediction(self, X, feature_names=None):
        """
        Explique une prédiction spécifique
        
        Args:
            X: Features pour une prédiction
            feature_names: Noms des features
            
        Returns:
            dict: Explication de la prédiction
        """
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné")
        
        prediction = self.predict(X)[0]
        
        if self.feature_importance is not None:
            # Top features contribuant à la prédiction
            top_features = self.feature_importance.head(5)
            
            explanation = {
                'prediction': prediction,
                'top_features': top_features.to_dict('records'),
                'model_type': self.model_type,
                'confidence': 'high' if prediction > 0 else 'low'
            }
        else:
            explanation = {
                'prediction': prediction,
                'model_type': self.model_type
            }
        
        return explanation
    
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
            'feature_importance': self.feature_importance,
            'training_metrics': self.training_metrics,
            'is_trained': self.is_trained,
            'timestamp': datetime.now().isoformat()
        }
        
        joblib.dump(model_data, filepath)
        _logger.info(f"Modèle sauvegardé: {filepath}")
    
    def load_model(self, filepath):
        """
        Charge un modèle sauvegardé
        
        Args:
            filepath: Chemin du modèle
        """
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.model_type = model_data['model_type']
        self.feature_importance = model_data['feature_importance']
        self.training_metrics = model_data['training_metrics']
        self.is_trained = model_data['is_trained']
        
        _logger.info(f"Modèle chargé: {filepath}")
    
    def get_model_info(self):
        """
        Retourne les informations du modèle
        
        Returns:
            dict: Informations du modèle
        """
        return {
            'model_type': self.model_type,
            'is_trained': self.is_trained,
            'training_metrics': self.training_metrics,
            'feature_count': len(self.feature_importance) if self.feature_importance is not None else 0,
            'top_features': self.get_feature_importance(5).to_dict('records') if self.feature_importance is not None else []
        }
