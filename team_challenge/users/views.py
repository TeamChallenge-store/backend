from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

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
