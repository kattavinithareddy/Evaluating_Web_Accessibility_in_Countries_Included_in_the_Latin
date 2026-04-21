from django.db import models
from django.utils import timezone

class MLModel(models.Model):
    MODEL_TYPES = (
        ('classification', 'Classification'),
        ('detection', 'Detection'),
        ('prediction', 'Prediction'),
        ('recommendation', 'Recommendation'),
    )
    
    model_name = models.CharField(max_length=255)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPES)
    version = models.CharField(max_length=50)
    file_path = models.FileField(upload_to='ml_models/')
    description = models.TextField()
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    training_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'ml_models'
    
    def __str__(self):
        return f"{self.model_name} v{self.version}"


class TrainingDataset(models.Model):
    dataset_name = models.CharField(max_length=255)
    description = models.TextField()
    file_path = models.FileField(upload_to='datasets/')
    total_records = models.IntegerField(default=0)
    features_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'training_datasets'
    
    def __str__(self):
        return self.dataset_name


class ModelPerformance(models.Model):
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='performance_metrics')
    evaluation_date = models.DateTimeField(default=timezone.now)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    precision = models.DecimalField(max_digits=5, decimal_places=2)
    recall = models.DecimalField(max_digits=5, decimal_places=2)
    f1_score = models.DecimalField(max_digits=5, decimal_places=2)
    metrics_data = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'model_performance'
    
    def __str__(self):
        return f"{self.model.model_name} - {self.evaluation_date}"
