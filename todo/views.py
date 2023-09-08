from django.shortcuts import render,get_object_or_404
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


class UserLoginView(APIView):

    def post(self,request):
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({'token': token.key, 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class CategoryListView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request):
        categories=Category.objects.filter(user=request.user)
        serializer=CategorySerializer(categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
            request.data['user']=request.user.id
            serializer=CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class TaskListView(APIView):
    def get(self,request):
        authentication_classes=[TokenAuthentication]
        permission_classes=[IsAuthenticated]

        params=request.query_params

        category=params.get('category',False)
        priority=params.get('priority',False)

        if category and priority:
            tasks =Task.objects.filter(user=request.user,category__name__icontains=category,priority__icontains=priority)
        else:
            tasks=Task.objects.filter(user=request.user)

        serializer=TaskSerializer(tasks,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def post(self,request):
        request.data['user']=request.user.id
        serializer=TaskCreateSerializer(data=request.data,context={'request': request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request,pk:int):
        task = get_object_or_404(Task,id=pk,user=request.user)

        serializer = TaskSerializer(task)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk:int):
        task=get_object_or_404(Task,id=pk,user=request.data)
        serializer=TaskSerializer(task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk):
        task=get_object_or_404(Task,id=pk,user=request.user)
        task.delete()
        return Response({"message": "Task has been deleted successfully."})