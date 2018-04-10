from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class CustomLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        #def login(self, request, redirect_url=None):
        #    pass

class PhoneChangeForm(forms.Form):

    phone = forms.CharField(label = 'New Phone Number', widget=forms.TextInput(attrs={'placeholder': 'New Number'}))

    def save(self, commit=True):
        instance = super(PhoneChangeForm, self).save(commit=False)
        phone = self.cleaned_data['phone']
        CustomUser.get()
        if commit:
            instance.save()
        return instance

class CustomUserCreationForm(forms.Form):

    phone = forms.CharField(label = 'Phone Number', widget=forms.TextInput(attrs={'placeholder': 'Ex: 1234567890'}))

    def signup(self, request, user):
        user.phone = self.cleaned_data['phone']
        user.save()

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
