from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from Authentication.models import PublicUsers

class ManageCreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password1',
			'password2',
			]

class ManagePublicUsersForm(forms.ModelForm):
	class Meta:
		model = PublicUsers
		fields = [
			'user' ,
			'contact' ,
			'address' ,
		]