from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name']

    def clean_password(self):
        password = self.cleaned_data['password']
        password_validation.validate_password(password, self.instance)
        return password

    def clean_first_name(self):
        name = self.cleaned_data['first_name']
        if not name:
            raise forms.ValidationError('Este campo é obrigatório.')
        return name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
