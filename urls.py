from django.contrib import admin
from django.urls import path, include
from security_app.views import home

urlpatterns = [
    path('', home, name='home'),  # Root/homepage URL
    path('admin/', admin.site.urls),  # Admin 
    path('api/', include('security_app.urls')), 
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
