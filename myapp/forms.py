from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    sex = forms.ChoiceField(choices=[('male', 'Мужчина'), ('female', 'Женщина')], label='sex')
    realname = forms.CharField(label='realname')

class AuthForm(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(widget=forms.PasswordInput, label='password')

class ReviewAddForm(forms.Form):
    title = forms.CharField(label='title')
    description = forms.CharField(label='description')
    product_barcode = forms.IntegerField(label='product_barcode')

class ReviewsSearch(forms.Form):
    barcode = forms.IntegerField(label='barcode')