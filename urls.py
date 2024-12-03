from django.contrib import admin
from django.urls import path, include
from security_app.views import home, UserDetailView, ProtectedViewJWT, ProtectedViewOAuth, check_admin_status

urlpatterns = [
    path('', home, name='home'),  # Root/homepage URL
    path('admin/', admin.site.urls),  # Admin 
    path('api/', include('security_app.urls')), 
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('protected/jwt/', ProtectedViewJWT.as_view(), name='protected-jwt'),
    path('protected/oauth/', ProtectedViewOAuth.as_view(), name='protected-oauth'),
    path('check-admin-status/', check_admin_status, name='check_admin_status'),
]
