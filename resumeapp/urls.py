from django.urls import path, include
from .import views


urlpatterns = [
	path('resume/', views.resume, name='resume'),
	path('portfolio', views.portfolio, name='portfolio'),
	path('resume2/', views.resume2, name='resume2'),
	path('portfolio_golfapp', views.portfolio_golfapp, name='portfolio-golfapp'),
]