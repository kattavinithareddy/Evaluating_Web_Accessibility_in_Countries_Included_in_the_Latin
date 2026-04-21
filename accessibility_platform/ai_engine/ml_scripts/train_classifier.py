import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from django.conf import settings

def train_accessibility_classifier():
    """
    Train a classifier to categorize accessibility issues
    """
    # Load dataset
    data = pd.read_csv(os.path.join(settings.DATASETS_DIR, 'accessibility_issues.csv'))
    
    # Prepare features and target
    X = data[['element_type', 'has_alt', 'has_label', 'has_aria', 'contrast_ratio', 'is_interactive']]
    y = data['issue_severity']
    
    # Encode categorical variables
    le = LabelEncoder()
    X['element_type'] = le.fit_transform(X['element_type'])
    y = le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    model_path = os.path.join(settings.ML_MODELS_DIR, 'accessibility_classifier.pkl')
    joblib.dump(model, model_path)
    print(f"\nModel saved to {model_path}")
    
    return accuracy

if __name__ == '__main__':
    train_accessibility_classifier()
