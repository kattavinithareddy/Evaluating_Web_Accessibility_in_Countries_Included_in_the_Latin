from django.db import models
from django.utils import timezone
from user_management.models import CustomUser
from compliance_evaluation.models import AccessibilityProject

class UserTestingProgram(models.Model):
    STATUS_CHOICES = (
        ('planning', 'Planning'),
        ('recruiting', 'Recruiting'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    project = models.ForeignKey(AccessibilityProject, on_delete=models.CASCADE, related_name='testing_programs')
    coordinator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='coordinated_tests')
    program_name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='planning')
    start_date = models.DateField()
    end_date = models.DateField()
    target_testers = models.IntegerField(default=5)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'user_testing_programs'
    
    def __str__(self):
        return f"{self.program_name} - {self.project.project_name}"


class Tester(models.Model):
    DISABILITY_TYPES = (
        ('visual', 'Visual Impairment'),
        ('hearing', 'Hearing Impairment'),
        ('motor', 'Motor Impairment'),
        ('cognitive', 'Cognitive Impairment'),
        ('none', 'No Disability'),
        ('multiple', 'Multiple Disabilities'),
    )
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='tester_profile')
    disability_type = models.CharField(max_length=50, choices=DISABILITY_TYPES)
    assistive_technologies = models.TextField(help_text="List of assistive technologies used")
    testing_experience = models.TextField()
    consent_given = models.BooleanField(default=False)
    consent_date = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'testers'
    
    def __str__(self):
        return f"Tester: {self.user.username} ({self.get_disability_type_display()})"


class TestTask(models.Model):
    TASK_STATUS = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
    )
    
    program = models.ForeignKey(UserTestingProgram, on_delete=models.CASCADE, related_name='tasks')
    tester = models.ForeignKey(Tester, on_delete=models.CASCADE, related_name='assigned_tasks')
    task_name = models.CharField(max_length=255)
    task_description = models.TextField()
    task_url = models.URLField(max_length=500)
    status = models.CharField(max_length=50, choices=TASK_STATUS, default='pending')
    assigned_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'test_tasks'
    
    def __str__(self):
        return f"{self.task_name} - {self.tester.user.username}"


class UserFeedback(models.Model):
    DIFFICULTY_LEVELS = (
        ('very_easy', 'Very Easy'),
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('difficult', 'Difficult'),
        ('very_difficult', 'Very Difficult'),
        ('impossible', 'Impossible'),
    )
    
    task = models.ForeignKey(TestTask, on_delete=models.CASCADE, related_name='feedback')
    difficulty_level = models.CharField(max_length=50, choices=DIFFICULTY_LEVELS)
    accessibility_barriers = models.TextField()
    positive_aspects = models.TextField(blank=True, null=True)
    suggestions = models.TextField(blank=True, null=True)
    time_taken = models.DurationField(null=True, blank=True)
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage of task completed")
    recorded_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'user_feedback'
    
    def __str__(self):
        return f"Feedback for {self.task.task_name}"
