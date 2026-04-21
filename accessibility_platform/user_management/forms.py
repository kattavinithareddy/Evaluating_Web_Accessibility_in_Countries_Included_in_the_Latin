from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    
    role = forms.ChoiceField(
        choices=[
            ('developer', 'Developer'),
            ('designer', 'Designer'),
            ('content_creator', 'Content Creator'),
            ('auditor', 'Auditor'),
            ('accessibility_advocate', 'Accessibility Advocate'),
            ('policymaker', 'Policymaker'),
            ('researcher', 'Researcher'),
            ('analyst', 'Analyst'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    organization_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Name'})
    )
    
    organization_type = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Select Type'),
            ('corporate', 'Corporate'),
            ('government', 'Government'),
            ('non_profit', 'Non-Profit'),
            ('education', 'Education'),
            ('healthcare', 'Healthcare'),
            ('other', 'Other'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'organization_name', 'organization_type']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'organization_name', 
                  'organization_type', 'profile_picture', 'accessibility_goals']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'organization_name': forms.TextInput(attrs={'class': 'form-control'}),
            'organization_type': forms.Select(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'accessibility_goals': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['notification_email', 'notification_in_app', 'report_format', 'theme_preference']
        widgets = {
            'notification_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notification_in_app': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'report_format': forms.Select(attrs={'class': 'form-control'}),
            'theme_preference': forms.Select(attrs={'class': 'form-control'}),
        }
