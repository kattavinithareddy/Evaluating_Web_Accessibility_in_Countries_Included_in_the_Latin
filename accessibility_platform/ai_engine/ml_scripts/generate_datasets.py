import pandas as pd
import numpy as np
import os
from django.conf import settings

def generate_accessibility_issues_dataset():
    """
    Generate synthetic accessibility issues dataset for training
    """
    np.random.seed(42)
    n_samples = 5000
    
    element_types = ['img', 'input', 'button', 'a', 'div', 'select', 'textarea']
    severities = ['critical', 'serious', 'moderate', 'minor']
    
    data = {
        'element_type': np.random.choice(element_types, n_samples),
        'has_alt': np.random.randint(0, 2, n_samples),
        'has_label': np.random.randint(0, 2, n_samples),
        'has_aria': np.random.randint(0, 2, n_samples),
        'contrast_ratio': np.random.uniform(1.0, 21.0, n_samples),
        'is_interactive': np.random.randint(0, 2, n_samples),
    }
    
    # Rule-based severity assignment
    severity = []
    for i in range(n_samples):
        if data['element_type'][i] == 'img' and data['has_alt'][i] == 0:
            severity.append('serious')
        elif data['element_type'][i] in ['input', 'select', 'textarea'] and data['has_label'][i] == 0:
            severity.append('serious')
        elif data['contrast_ratio'][i] < 3.0:
            severity.append('critical')
        elif data['contrast_ratio'][i] < 4.5:
            severity.append('moderate')
        elif data['is_interactive'][i] == 1 and data['has_aria'][i] == 0:
            severity.append('moderate')
        else:
            severity.append('minor')
    
    data['issue_severity'] = severity
    
    df = pd.DataFrame(data)
    
    # Save dataset
    dataset_path = os.path.join(settings.DATASETS_DIR, 'accessibility_issues.csv')
    os.makedirs(settings.DATASETS_DIR, exist_ok=True)
    df.to_csv(dataset_path, index=False)
    
    print(f"Accessibility issues dataset generated: {dataset_path}")
    print(f"Total samples: {len(df)}")
    print(f"\nSeverity distribution:")
    print(df['issue_severity'].value_counts())
    
    return df

def generate_compliance_dataset():
    """
    Generate compliance scores dataset
    """
    np.random.seed(42)
    n_samples = 3000
    
    data = {
        'critical_issues': np.random.randint(0, 20, n_samples),
        'serious_issues': np.random.randint(0, 50, n_samples),
        'moderate_issues': np.random.randint(0, 100, n_samples),
        'minor_issues': np.random.randint(0, 150, n_samples),
        'total_elements': np.random.randint(50, 1000, n_samples),
        'wcag_level': np.random.choice([0, 1, 2], n_samples),  # A=0, AA=1, AAA=2
    }
    
    # Calculate compliance score
    compliance_scores = []
    for i in range(n_samples):
        total_issues = (data['critical_issues'][i] * 4 + 
                       data['serious_issues'][i] * 3 + 
                       data['moderate_issues'][i] * 2 + 
                       data['minor_issues'][i])
        
        max_penalty = data['total_elements'][i] * 2
        score = max(0, 100 - (total_issues / max_penalty * 100))
        compliance_scores.append(score)
    
    data['compliance_score'] = compliance_scores
    
    df = pd.DataFrame(data)
    
    # Save dataset
    dataset_path = os.path.join(settings.DATASETS_DIR, 'compliance_data.csv')
    df.to_csv(dataset_path, index=False)
    
    print(f"\nCompliance dataset generated: {dataset_path}")
    print(f"Total samples: {len(df)}")
    print(f"\nCompliance score statistics:")
    print(df['compliance_score'].describe())
    
    return df

if __name__ == '__main__':
    # Create datasets directory
    os.makedirs(settings.DATASETS_DIR, exist_ok=True)
    
    print("Generating datasets...")
    generate_accessibility_issues_dataset()
    generate_compliance_dataset()
    print("\nAll datasets generated successfully!")
