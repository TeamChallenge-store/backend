from django.urls import path, include
from .views import RegisterView, LoginAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)                   

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path ('sign-up/', RegisterView.as_view(), name='register'),
    path ('sign-in/', LoginAPIView.as_view(), name='login'),
    path('auth/', include('djoser.urls')),
]