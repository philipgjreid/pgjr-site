from django.urls import path, include
from .import views


urlpatterns = [
	path('resumeOLD/', views.resume, name='resume'),
	path('resume/', views.resume2, name='resume2'),
	path('portfolio', views.portfolio, name='portfolio'),
	path('portfolio_golfapp', views.portfolio_golfapp, name='portfolio-golfapp'),
]