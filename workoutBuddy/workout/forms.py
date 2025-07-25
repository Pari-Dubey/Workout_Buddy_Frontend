from django import forms

class CreateWorkoutForm(forms.Form):
    age = forms.IntegerField(min_value=1)
    gender = forms.ChoiceField(choices=[("male", "Male"), ("female", "Female"), ("other", "Other")])
    height_cm = forms.FloatField(min_value=0)
    weight_kg = forms.FloatField(min_value=0)
    goal = forms.ChoiceField(choices=[
        ("lose_weight", "Lose Weight"),
        ("gain_muscle", "Gain Muscle"),
        ("improve_fitness","Improve Fitness"),
        ("maintain", "Maintain Fitness")
    ])
    activity_level = forms.ChoiceField(choices=[
        ("sedentary", "Sedentary"),
        ("lightly_active" , "Lightly Active"),
        ("moderately_active", "Moderately Active"),
        ("very_active", "Very Active")
    ])
    workout_days_per_week = forms.IntegerField(min_value=0, max_value=7)
    workout_duration = forms.CharField()  # e.g. "30 minutes"

    # These are optional and comma-separated
    medical_conditions = forms.CharField(required=False, widget=forms.Textarea)
    injuries_or_limitations = forms.CharField(required=False, widget=forms.Textarea)