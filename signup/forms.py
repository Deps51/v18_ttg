from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    #first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
   #last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Email is required in order to notify you about product updates!.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

'''class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('url', 'location', 'company')'''
