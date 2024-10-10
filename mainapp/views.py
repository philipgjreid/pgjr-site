from django.shortcuts import render, redirect


def home(request):
	return render(request, 'mainapp/home.html', {})

def home2(request):
	return render(request, 'mainapp/home2.html', {})
