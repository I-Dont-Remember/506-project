from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator

class CustomLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        #def login(self, request, redirect_url=None):
        #    pass
my_default_sign_up_phone_number_errors = {
    'required': 'This field is required',
    'invalid': 'Enter a 10-digit phone number below.'
}
my_default_change_phone_number_errors = {
    'required': 'This field is required',
    'invalid': 'Your new phone number must be exactly 10-digit long'
}
class PhoneChangeForm(forms.Form):

    phone = forms.IntegerField(
            error_messages=my_default_change_phone_number_errors,
            label = 'New Phone Number',
            widget=forms.TextInput(
            attrs={'placeholder': '10-digit phone number'}),
            validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)]

    )

    def save(self, commit=True):
        instance = super(PhoneChangeForm, self).save(commit=False)
        phone = self.cleaned_data['phone']
        CustomUser.get()
        if commit:
            instance.save()
        return instance

class CustomUserCreationForm(forms.Form):

    phone = forms.IntegerField(
            error_messages=my_default_sign_up_phone_number_errors,
            label = 'Phone Number',
            widget=forms.TextInput(
            attrs={'placeholder': '10-digit phone number'}),
            validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)]

    )

    def signup(self, request, user):
        user.phone = self.cleaned_data['phone']
        user.twilio_phone = '13312156629'
        user.save()

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
