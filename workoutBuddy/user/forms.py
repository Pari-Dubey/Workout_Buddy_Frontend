from django import forms

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))



class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}), required=True)


class ProfileForm(forms.Form):
    full_name = forms.CharField(required=True)
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        required=True
    )
    height = forms.FloatField(required=True)
    weight = forms.FloatField(required=True)

    activity_level = forms.ChoiceField(
        choices=[
            ('sedentary', 'Sedentary'),
            ('light', 'Lightly Active'),
            ('moderate', 'Moderately Active'),
            ('active', 'Active'),
            ('very_active', 'Very Active'),
        ],
        required=True
    )

    goal = forms.ChoiceField(
        choices=[
            ('lose_weight', 'Lose Weight'),
            ('gain_muscle', 'Gain Muscle'),
            ('maintain_fitness', 'Maintain Fitness'),
        ],
        required=True
    )
