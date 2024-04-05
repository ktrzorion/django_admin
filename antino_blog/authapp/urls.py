from django.urls import path
from . import views
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserLogoutView, UserChangePasswordView, UserPasswordResetView
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    # path('', views.getRoutes),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change-password/', UserChangePasswordView.as_view(), name='change_password'),
    # path('reset-email/', SendPasswordResetEmailView.as_view(), name='password_reset_email'),
    path('reset/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset_password'),
]