from django.shortcuts import render

def resume(request):
	return render(request, 'resumeapp/resume.html', {})

def resume2(request):
	return render(request, 'resumeapp/resume2.html', {})

def portfolio(request):
	return render(request, 'resumeapp/portfolio.html', {})

def portfolio_golfapp(request):
	return render(request, 'resumeapp/portfolio-golfapp.html', {})

def portfolio_website(request):
	return render(request, 'resumeapp/portfolio-website.html', {})
