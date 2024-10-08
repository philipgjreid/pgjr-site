from django.urls import path
from .import views

urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register-user'),
    path('guest_login', views.guest_login, name='guest-login'),
    # path('delete_guest_user/', views.delete_guest_user, name='delete-guest-user'),
]