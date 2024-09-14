from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from userauths.models import User, Profile
from userauths.serializer import RegisterSerializer, MyTokenObtainPairSerializer

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT token pair.
    """
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer