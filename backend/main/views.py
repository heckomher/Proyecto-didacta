from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, LoginSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        if User.objects.exists() and (not request.user.is_authenticated or request.user.role != 'UTP'):
            return Response({"error": "Only UTP can register new users."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # For JWT, logout is handled on client side by removing token
    return Response({"message": "Logged out successfully."})

# Create your views here.
