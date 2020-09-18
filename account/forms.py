from django import forms
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
	username = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
	password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))

class PwdChangeForm(PasswordChangeForm):
	old_password= forms.CharField(widget=PasswordInput(attrs={'id':'old_password','class': 'form-control','placeholder':'Password'}))
	new_password1= forms.CharField(widget=PasswordInput(attrs={'id':'new_password1','class': 'form-control','placeholder':'Password'}))
	new_password2= forms.CharField(widget=PasswordInput(attrs={'id':'new_password2','class': 'form-control','placeholder':'Password'}))

class UserRegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Pasword',widget=forms.PasswordInput)
	password2 = forms.CharField(label='Repeat Pasword',widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username','first_name','email')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise form.ValidationError('Passwords do not match')
		return cd['password2']