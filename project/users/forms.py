from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    phone = forms.CharField(label = 'Phone Number')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone')

    #def save(self, commit=True):
    #        raise NotImplementedError('Must save CustomUser before extending it!')
    #    user = super(UserCreateForm, self).save(commit=True)
    #    mod_user = CustomUser.get(username=user.username)
    #    mod_user.save()
    #    return mod_user

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
