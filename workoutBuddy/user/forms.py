from django import forms
from django.core.exceptions import ValidationError
import re

class RegisterForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'id': 'signup-email'
        }),
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address',
        }
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'password-input',
            'autocomplete': 'off'
        }),
        error_messages={
            'required': 'Password is required.',
        }
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'id': 'login-email'}),
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
        }
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'password-input',
            'autocomplete': 'off'
        }),
        error_messages={
            'required': 'Password is required.',
        }
    )


class ProfileForm(forms.Form):
    
    full_name = forms.CharField(
        max_length=50,
        error_messages={
            'required': 'Full name is required.',
            'max_length': 'Full name must be 50 characters or fewer.'
        }
    )

    age = forms.IntegerField(
        min_value=10,
        max_value=100,
        error_messages={
            'required': 'Please enter your age.',
            'min_value': 'Age must be at least 10.',
            'max_value': 'Age must be 100 or less.',
            'invalid': 'Enter a valid age.'
        }
    )

    gender = forms.ChoiceField(
        choices=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other")
        ],
        error_messages={
            'required': 'Please select your gender.',
            'invalid_choice': 'Choose a valid gender.'
        }
    )

    height = forms.FloatField(
        min_value=50,
        max_value=250,
        error_messages={
            'required': 'Please enter your height.',
            'min_value': 'Height must be at least 50 cm.',
            'max_value': 'Height cannot exceed 250 cm.',
            'invalid': 'Enter a valid number for height.'
        }
    )

    weight = forms.FloatField(
        min_value=20,
        max_value=200,
        error_messages={
            'required': 'Please enter your weight.',
            'min_value': 'Weight must be at least 20 kg.',
            'max_value': 'Weight cannot exceed 200 kg.',
            'invalid': 'Enter a valid number for weight.'
        }
    )

    activity_level = forms.ChoiceField(
    choices=[
        ("sedentary", "Sedentary"),
        ("light", "Light"),
        ("moderate", "Moderate"),
        ("active", "Active"),
        ("very_active", "Very Active"),
    ],
    error_messages={
        'required': 'Please select your activity level.',
        'invalid_choice': 'Choose a valid activity level.'
    }
    )

    goal = forms.ChoiceField(
        choices=[
            ("lose_weight", "Lose Weight"),
            ("gain_muscle", "Gain Muscle"),
            ("maintain_fitness", "Maintain Fitness"),
        ],
        error_messages={
            'required': 'Please choose your fitness goal.',
            'invalid_choice': 'Choose a valid goal.'
        }
    )

    
    def clean_full_name(self):
        name = self.cleaned_data.get('full_name')
        if not re.match(r'^[A-Za-z ]+$', name):
            raise ValidationError("Only letters and spaces are allowed.")
        return name