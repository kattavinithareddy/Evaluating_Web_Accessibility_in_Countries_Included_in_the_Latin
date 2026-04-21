from django import forms
from .models import AccessibilityProject
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class AccessibilityProjectForm(forms.ModelForm):
    class Meta:
        model = AccessibilityProject
        fields = ['project_name', 'project_type', 'url', 'description', 'wcag_level_target']
        widgets = {
            'project_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project name'
            }),
            'project_type': forms.Select(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your project...'
            }),
            'wcag_level_target': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url:
            validator = URLValidator()
            try:
                validator(url)
            except ValidationError:
                raise ValidationError('Enter a valid URL starting with http:// or https://')
            
            if not (url.startswith('http://') or url.startswith('https://')):
                raise ValidationError('URL must start with http:// or https://')
        return url
    
    def clean_project_name(self):
        project_name = self.cleaned_data.get('project_name')
        if len(project_name) < 3:
            raise ValidationError('Project name must be at least 3 characters long.')
        return project_name
