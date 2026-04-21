from django import forms
from .models import UserTestingProgram, Tester, TestTask, UserFeedback
from compliance_evaluation.models import AccessibilityProject

class UserTestingProgramForm(forms.ModelForm):
    class Meta:
        model = UserTestingProgram
        fields = ['project', 'program_name', 'description', 'status', 
                  'start_date', 'end_date', 'target_testers']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'program_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'target_testers': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['project'].queryset = AccessibilityProject.objects.filter(user=self.user)
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError('End date must be after start date.')
        
        return cleaned_data

class TesterForm(forms.ModelForm):
    class Meta:
        model = Tester
        fields = ['disability_type', 'assistive_technologies', 'testing_experience', 'consent_given']
        widgets = {
            'disability_type': forms.Select(attrs={'class': 'form-control'}),
            'assistive_technologies': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., JAWS, NVDA, VoiceOver, ZoomText'
            }),
            'testing_experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your testing experience...'
            }),
            'consent_given': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_consent_given(self):
        consent = self.cleaned_data.get('consent_given')
        if not consent:
            raise forms.ValidationError('You must provide consent to participate in testing.')
        return consent

class TestTaskForm(forms.ModelForm):
    class Meta:
        model = TestTask
        fields = ['tester', 'task_name', 'task_description', 'task_url']
        widgets = {
            'tester': forms.Select(attrs={'class': 'form-control'}),
            'task_name': forms.TextInput(attrs={'class': 'form-control'}),
            'task_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'task_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class UserFeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ['difficulty_level', 'accessibility_barriers', 'positive_aspects', 
                  'suggestions', 'success_rate']
        widgets = {
            'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
            'accessibility_barriers': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe barriers encountered...'
            }),
            'positive_aspects': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What worked well...'
            }),
            'suggestions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Suggestions for improvement...'
            }),
            'success_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'step': 0.01
            }),
        }
