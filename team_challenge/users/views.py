from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed


class RegisterView(APIView):

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user) 

            refresh.payload.update({    
                'user_id': user.id,
                'username': user.username
            })

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token), 
            }, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    def post(self, request):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        if username is None or password is None:
            return Response({'error': 'Username and password are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed({'error': 'Invalid credentials'}, code=status.HTTP_401_UNAUTHORIZED)

        # Перевіряємо пароль за допомогою методу check_password
        if not user.check_password(password):
            raise AuthenticationFailed({'error': 'Invalid credentials'}, code=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username
        })

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    
class LogoutAPIView(APIView):

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token is required'},

                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist() # Add it to the blacklist

        except Exception as e:
            return Response({'error': 'Invalid Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'success': 'Logout successful'}, status=status.HTTP_200_OK)