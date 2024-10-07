from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
    path('', include('roundapp.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('membersapp.urls')),
    path('', include('resumeapp.urls')),
]
