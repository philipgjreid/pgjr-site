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

def portfolio_powerapps(request):
	return render(request, 'resumeapp/portfolio-powerapps.html', {})

def portfolio_powerbi(request):
	return render(request, 'resumeapp/portfolio-powerbi.html', {})

def portfolio_tableau(request):
	return render(request, 'resumeapp/portfolio-tableau.html', {})

def portfolio_tableau_F1(request):
	return render(request, 'resumeapp/portfolio-tableau-F1.html', {})
