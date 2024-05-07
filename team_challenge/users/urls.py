from django.urls import path, include
from rest_framework_simplejwt import views
                 

urlpatterns = [
    path('auth', include('djoser.urls')),
    
    path('jwt/create', views.TokenObtainPairView.as_view(), name="jwt-create"),
    path('jwt/refresh', views.TokenRefreshView.as_view(), name="jwt-refresh"),
    path('jwt/verify', views.TokenVerifyView.as_view(), name="jwt-verify"),
]