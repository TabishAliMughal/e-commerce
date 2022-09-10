from re import A
from unicodedata import name
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .user_handeling import unauthenticated_user
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random

def ManageUserLoginView(LoginView):
	if LoginView.method == 'POST':
		username = LoginView.POST.get('username')
		password =LoginView.POST.get('password')
		user = authenticate(LoginView, username=username, password=password)
		if user is not None:
			login(LoginView, user)
			return redirect('auth:profile')
		else:
			context = {
				'msg' : 'Username Or Password Is Incorrect',
			}
			return render(LoginView , 'Authentication/Login.html' , context)
	else:
		return render(LoginView , 'Authentication/Login.html')

@login_required(login_url='auth:login')
def ManageUserLogoutView(request):
	logout(request)
	return redirect('products:listview')

@unauthenticated_user
def ManageUserRegisterView(RegisterView):
	form = ManageCreateUserForm()
	if RegisterView.method == 'POST':
		form = ManageCreateUserForm({
			'username' : RegisterView.POST.get('u-name') ,
			'email' : RegisterView.POST.get('email') ,
			'password1' : RegisterView.POST.get('password1') ,
			'password2' : RegisterView.POST.get('password2') ,
		})
		if form.is_valid():
			user = form.save()
			
			send_mail(
				'This Email Has Been Redistered',
				'This Email Has Been Redistered On An E-Commerce Website',
				'ztapp000@gmail.com',
				[str(RegisterView.POST.get('email'))],
				fail_silently=True,
			)
			username = form.cleaned_data.get('username')
			group = Group.objects.get(name='Public')
			user.groups.add(group)
			messages.success(RegisterView, 'Account was created for ' + username)
			return redirect('auth:profile')
		else:
			if str(RegisterView.POST.get('u-name')) in [i.username for i in User.objects.all()]:
				msg1 = "User With This Username Already Exist"
			if str(RegisterView.POST.get('password1')) == str(RegisterView.POST.get('password2')):
				msg2 = "Passwords Does Not Match"
			context = {
				'msg1': msg1 ,
				'msg2': msg2 ,
				'form': form ,
				}
			return render(RegisterView, 'Authentication/Register.html', context)
	else:
		context = {
			'form' : ManageCreateUserForm() ,
		}
		return render(RegisterView , 'Authentication/Register.html', context)

@login_required(login_url='auth:login')
def ManageEmailConfirmationView(EmailView):
	if EmailView.method == 'POST':
		code = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
		random.shuffle(code)
		confirmation = ""
		for i in range(1,9):
			confirmation = confirmation + code[i]
		if str(EmailView.POST.get('email')) != str(EmailView.user.email):
			send_mail(
				'Confirm Email Code',
				'This Email Has Been Updated On An E-Commerce Website. \n Confirmation Code is : {}'.format(confirmation),
				'ztapp000@gmail.com',
				[str(EmailView.POST.get('email'))],
				fail_silently=True,
			)
	EmailView.session['confirmation'] = confirmation
	print(EmailView.session.get('confirmation'))
	return render(EmailView , 'Authentication/Profile.html')
		

@login_required(login_url='auth:login')
def ManageUserProfileView(ProfileView):
	if ProfileView.method == 'POST':
		try:
			instance = get_object_or_404(PublicUsers , user = ProfileView.user)
		except:
			instance = None
		publicuserform = ManagePublicUsersForm({
			'user' : ProfileView.user ,
			'contact' : ProfileView.POST.get('contact') ,
			'address' : ProfileView.POST.get('address') ,
		} or None , instance = instance )
		publicuserform.save()
		if str(ProfileView.POST.get('email')) != str(ProfileView.user.email):
			if ProfileView.POST.get('code') == ProfileView.session.get('confirmation'):
				previous_email = ProfileView.user.email
				ProfileView.user.email = ProfileView.POST.get('email')
				ProfileView.user.save()
				send_mail(
					'This Email Has Been Updated',
					'This Email Has Been Updated On An E-Commerce Website. \n Previous Email Was {}'.format(previous_email),
					'ztapp000@gmail.com',
					[str(ProfileView.POST.get('email'))],
					fail_silently=True,
				)
		form = ManagePublicUsersForm(get_object_or_404(PublicUsers , user = ProfileView.user))
		context = {
			'form' : form ,
		}
		return render(ProfileView , 'Authentication/Profile.html')
	else:
		try:
			form = ManagePublicUsersForm(instance = get_object_or_404(PublicUsers , user = ProfileView.user))
		except:
			form = ManagePublicUsersForm()
		context = {
			'form' : form ,
		}
		return render(ProfileView , 'Authentication/Profile.html' , context)
# @admin_only
# @login_required(login_url='main_login')
# @allowed_users(allowed_roles=['admin'])