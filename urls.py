from django.urls import path
from .views import (
    RegisterUserView,
    UserListView,
    UserDetailView,
    login_user,
    LoginView,
    ProtectedViewJWT,
    ProtectedViewOAuth,
    check_admin_status,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # route el authentification
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login w obtain tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('register/', RegisterUserView.as_view(), name='register'),  # Register user jdid

    # routes teb3in el users
    path('users/', UserListView.as_view(), name='user-list'),  # List and create users
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),  # get/Update/Delete user bl ID
    path('check-admin-status/', check_admin_status, name='check_admin_status'),

    # Protected routes
    #path('protected/', ProtectedView.as_view(), name='protected'),  # Protected route requiring auth
    path('protected/jwt/', ProtectedViewJWT.as_view(), name='protected-jwt'),
    path('protected/oauth/', ProtectedViewOAuth.as_view(), name='protected-oauth'),
]
