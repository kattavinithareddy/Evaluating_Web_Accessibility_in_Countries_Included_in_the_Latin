from django.core.management.base import BaseCommand
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../ml_scripts'))
from train_classifier import train_accessibility_classifier
from train_compliance_predictor import train_compliance_predictor

class Command(BaseCommand):
    help = 'Train ML models for accessibility detection'
    
    def handle(self, *args, **options):
        self.stdout.write('Training accessibility classifier...')
        acc = train_accessibility_classifier()
        self.stdout.write(self.style.SUCCESS(f'Classifier trained with accuracy: {acc:.4f}'))
        
        self.stdout.write('\nTraining compliance predictor...')
        r2 = train_compliance_predictor()
        self.stdout.write(self.style.SUCCESS(f'Predictor trained with R2 score: {r2:.4f}'))
        
        self.stdout.write(self.style.SUCCESS('\nAll models trained successfully!'))
