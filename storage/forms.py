from django import forms
from django.contrib.auth.models import User

from .models import Person, Address, Phone, Email


class AddPersonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'placeholder': 'Add first name...'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Add last name...'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Add description here...'})

    class Meta:
        fields = ('first_name', 'last_name', 'description')
        model = Person


class AddAddressForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['city'].widget.attrs.update({'placeholder': 'Add city name...'})
        self.fields['street'].widget.attrs.update({'placeholder': 'Add street name...'})
        self.fields['house_number'].widget.attrs.update({'placeholder': 'Add house number...'})
        self.fields['flat_number'].widget.attrs.update({'placeholder': 'Add flat number...'})

    class Meta:
        fields = ('city', 'street', 'house_number', 'flat_number', )
        model = Address


class AddPhoneForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['number'].widget.attrs.update({'placeholder': 'Add phone number...'})

    class Meta:
        fields = ('number', 'number_type', )
        model = Phone


class AddEmailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['address'].widget.attrs.update({'placeholder': 'Add email address...'})

    class Meta:
        fields = ('address', 'email_type', )
        model = Email


class LoginForm(forms.Form):

    email = forms.EmailField(label='')
    password = forms.CharField(label='', max_length=64, widget=forms.PasswordInput)

    email.widget.attrs.update({'placeholder': 'E-mail', 'required': True})
    password.widget.attrs.update({'placeholder': 'Password', 'required': True})


class RegisterForm(forms.ModelForm):

    password = forms.CharField(label='', max_length=64, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password...'}),)
    password_confirmation = forms.CharField(label='', max_length=64, required=True,
                                            widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password confirmation..'}),)

    class Meta:

        fields = ('first_name', 'last_name', 'email')
        model = User
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter your first name...'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter your last name...'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your e-mail address...'})

    def clean(self):

        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        email = self.cleaned_data['email']
        user_search = User.objects.filter(email=email)

        if user_search:
            self.add_error('email', 'This e-mail address is already taken')

        if password != password_confirmation:
            self.add_error('password_confirmation', 'the passwords you provide are not the same. Please try again')

    def save(self, commit=True):
        user = super().save(commit=commit)
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user.set_password(password)
        user.username = email
        user.save()
        return user



