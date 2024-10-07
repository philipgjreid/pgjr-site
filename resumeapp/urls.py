from django.urls import path, include
from .import views


urlpatterns = [
	path('resume/', views.resume, name='resume'),
	path('portfolio', views.portfolio, name='portfolio'),
]