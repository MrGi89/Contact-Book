from django import forms

from .models import Person, Address, Phone, Email


class AddPersonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'placeholder': 'Add first name...'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Add last name...'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Add description here...'})

    class Meta:
        fields = '__all__'
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


class RegisterForm(forms.Form):

    first_name = forms.CharField(label='', max_length=64)
    last_name = forms.CharField(label='', max_length=64)
    email = forms.EmailField(label='')
    password = forms.CharField(label='', max_length=64, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='', max_length=64, widget=forms.PasswordInput)

    first_name.widget.attrs.update({'placeholder': 'First name', 'required': True})
    last_name.widget.attrs.update({'placeholder': 'Last name', 'required': True})
    email.widget.attrs.update({'placeholder': 'E-mail', 'required': True})
    password.widget.attrs.update({'placeholder': 'Password', 'required': True})
    password_confirmation.widget.attrs.update({'placeholder': 'Password confirmation', 'required': True})
