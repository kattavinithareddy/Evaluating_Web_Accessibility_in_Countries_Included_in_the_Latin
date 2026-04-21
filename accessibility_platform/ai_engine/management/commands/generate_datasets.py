from django.core.management.base import BaseCommand
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../ml_scripts'))
from generate_datasets import generate_accessibility_issues_dataset, generate_compliance_dataset

class Command(BaseCommand):
    help = 'Generate training datasets for ML models'
    
    def handle(self, *args, **options):
        self.stdout.write('Generating datasets...')
        generate_accessibility_issues_dataset()
        generate_compliance_dataset()
        self.stdout.write(self.style.SUCCESS('Datasets generated successfully!'))
