from django.urls import path, include
from .import views


urlpatterns = [
	path('resumeOLD/', views.resume, name='resumeOLD'),
	path('resume/', views.resume2, name='resume'),
	path('portfolio', views.portfolio, name='portfolio'),
	path('portfolio_golfapp', views.portfolio_golfapp, name='portfolio-golfapp'),
	path('portfolio_website', views.portfolio_website, name='portfolio-website'),
	path('portfolio_powerapps', views.portfolio_powerapps, name='portfolio-powerapps'),
	path('portfolio_powerbi', views.portfolio_powerbi, name='portfolio-powerbi'),
	path('portfolio_tableau', views.portfolio_tableau, name='portfolio-tableau'),
	path('portfolio_tableau_F1', views.portfolio_tableau_F1, name='portfolio-tableau-F1'),
]