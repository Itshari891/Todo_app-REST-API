from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import (UserSerializer,
                        TodoSerializer,
                        TodoListSerializer,)
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User=get_user_model()
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class RegisterAPIView(APIView):

    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data["username"]=account.username
            data["email"]=account.email
            token,create=Token.objects.get_or_create(user=account)
            data["token"]=token.key
            return Response(data)
        return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)

class TodoAddAPIView(APIView):
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)

    def post(self,request,*args,**kwargs):
        serializer=TodoSerializer(data=request.data)
        user=request.user
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data)
        return Response(serializer.errors)

class TodoListAPIView(APIView):
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)

    def get(self,request,*args,**kwargs):
        user=request.user
        todos=user.todo_set.all()
        serializer=TodoListSerializer(todos,many=True)
        return Response(serializer.data)

class TodoDetailAPIView(APIView):
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)

    def get(self,request,*args,**kwargs):
        user=request.user
        id=kwargs.get("id")
        try:
            todo=user.todo_set.get(id=id)
            serializer=TodoListSerializer(todo)
            return Response(serializer.data)
        except:
            return Response({"message":"no such todo"})
    
    def put(self,request,*args,**kwargs):
        user=request.user
        id=kwargs.get("id")
        try:
            serializer=TodoListSerializer(data=request.data)
            if serializer.is_valid():
                todo=user.todo_set.get(id=id)
                todo.status=serializer.validated_data["status"]
                todo.save()
                if serializer.validated_data["status"]==True:
                    return Response({"message":"completed"})
                else:
                    return Response({"message":"pending"})
            return Response(serializer.errors)
        except:
            return Response({"message":"no such todo"})

    def delete(self,request,*args,**kwargs):
        user=request.user
        id=kwargs.get("id")
        try:
            todo=user.todo_set.get(id=id)
            todo.delete()
            return Response({"message":"todo deleted"})
        except:
            return Response({"message":"no such todo"})
    
    
