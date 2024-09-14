from django.shortcuts import render

from rest_framework_simplejwt.views import TokenObtainPairView
from userauths.models import User, Profile
from userauths.serializer import RegisterSerializer, myTokenObtainPairSerializer

# Create your views here.
class myTokenObtainPairView(TokenObtainPairView):
    serializer_class = myTokenObtainPairSerializer