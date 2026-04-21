from django import forms
from .models import AccessibilityRule, SystemConfiguration

class AccessibilityRuleForm(forms.ModelForm):
    class Meta:
        model = AccessibilityRule
        fields = ['rule_id', 'wcag_criterion', 'wcag_level', 'rule_name', 
                  'description', 'testing_procedure', 'weight', 'severity_default', 'is_active']
        widgets = {
            'rule_id': forms.TextInput(attrs={'class': 'form-control'}),
            'wcag_criterion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1.1.1'}),
            'wcag_level': forms.Select(attrs={'class': 'form-control'}),
            'rule_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'testing_procedure': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'severity_default': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SystemConfigurationForm(forms.ModelForm):
    class Meta:
        model = SystemConfiguration
        fields = ['config_key', 'config_value', 'description']
        widgets = {
            'config_key': forms.TextInput(attrs={'class': 'form-control'}),
            'config_value': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
