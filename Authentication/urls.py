from django.urls import path
from . import views

app_name = 'Authentication'

urlpatterns = [
	path('login/', views.ManageUserLoginView, name="login"),
	path('logout/', views.ManageUserLogoutView, name="logout"),
	path('register/', views.ManageUserRegisterView, name="register"),
	path('profile/', views.ManageUserProfileView, name="profile"),
	path('send-mail/', views.ManageEmailConfirmationView, name="email"),
]