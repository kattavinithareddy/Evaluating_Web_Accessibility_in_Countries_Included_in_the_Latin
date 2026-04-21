import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from django.conf import settings

def train_compliance_predictor():
    """
    Train a model to predict compliance scores
    """
    # Load dataset
    data = pd.read_csv(os.path.join(settings.DATASETS_DIR, 'compliance_data.csv'))
    
    # Features: issue counts by severity, wcag level, etc.
    X = data[['critical_issues', 'serious_issues', 'moderate_issues', 
              'minor_issues', 'total_elements', 'wcag_level']]
    y = data['compliance_score']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model MSE: {mse:.4f}")
    print(f"Model R2 Score: {r2:.4f}")
    
    # Save model
    model_path = os.path.join(settings.ML_MODELS_DIR, 'compliance_predictor.pkl')
    joblib.dump(model, model_path)
    print(f"\nModel saved to {model_path}")
    
    return r2

if __name__ == '__main__':
    train_compliance_predictor()
