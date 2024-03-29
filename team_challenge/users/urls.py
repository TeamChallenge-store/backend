from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)                   

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path ('sign-up/', RegisterView.as_view(), name='register'),
    path ('sign-in/', RegisterView.as_view(), name='login'),
]