from django import forms
from .models import MonitoringSchedule, AlertRule

class MonitoringScheduleForm(forms.ModelForm):
    class Meta:
        model = MonitoringSchedule
        fields = ['frequency', 'notification_enabled']
        widgets = {
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'notification_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AlertRuleForm(forms.ModelForm):
    class Meta:
        model = AlertRule
        fields = ['rule_name', 'condition', 'is_active']
        widgets = {
            'rule_name': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter condition as JSON'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
