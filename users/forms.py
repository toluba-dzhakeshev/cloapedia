from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile


class ProfileRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Profile
        fields = UserCreationForm.Meta.fields + ('phone',)

    def __init__(self, *args, **kwargs):
        super(ProfileRegistrationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'phone', 'email', 'description', 'image']
