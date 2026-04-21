from django import forms
from .models import Report

class ReportGenerationForm(forms.Form):
    report_type = forms.ChoiceField(
        choices=[
            ('compliance', 'Compliance Report'),
            ('trend_analysis', 'Trend Analysis'),
            ('user_testing', 'User Testing Report'),
            ('comparison', 'Comparison Report'),
            ('executive_summary', 'Executive Summary'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    report_format = forms.ChoiceField(
        choices=[
            ('pdf', 'PDF'),
            ('excel', 'Excel'),
            ('html', 'HTML'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    include_resolved = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Include resolved issues'
    )
