from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from roundapp.models import Round
# from django.http import JsonResponse


def login_user(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('check-incomplete-rounds')
		else:
			messages.success(request, ("There Was An Error Logging In, Try Again..."))
			return	redirect('login')
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	guest_user = request.user
	logout(request)
	if guest_user.username.startswith('guest_'):
		# Delete guest data
		Round.objects.filter(player=guest_user).delete()
		guest_user.delete()
	messages.success(request, ("You Were Logged Out..."))
	return redirect('golf-home')

def register_user(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Registration successful"))
			return redirect('home')
	else:
		form = RegisterUserForm()
	return render(request, 'authenticate/register_user.html', {'form': form})

def guest_login(request):
	# Generate a unique guest username
	guest_username = f'guest_{get_random_string(8)}'
	guest_user = User.objects.create_user(username=guest_username, password='guest_password', first_name="Guest")
	login(request, guest_user)
	return redirect('golf-home')

# Attempts to delete guest users when they navigate away did not work so will keep it manual. Logout works though.
# def delete_guest_user(request):
# 	if request.user.is_authenticated and request.user.username.startswith('guest_'):
# 		guest_user = request.user
# 		Round.objects.filter(player=guest_user).delete()
# 		guest_user.delete()
# 		return JsonResponse({'status': 'success'})
# 	return JsonResponse({'status': 'error'}, status=400)

