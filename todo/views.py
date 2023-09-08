from django.shortcuts import render
from .models import Category,Task
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.request import Request
from rest_framework.response import  Response
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token 
# Create your views here.
from .serializers import (UserRegisterSerializer,TaskCreateSerializer,CategorySerializer,TaskSerializer)


class UserRegistrationView(APIView):
    def post(self,request):

        serializer=UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token=Token.objects.get_or_create(user=user)
            return Response({'token':token.key,'message':'user registered successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    