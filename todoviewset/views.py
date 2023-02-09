from django.shortcuts import render,get_object_or_404
from todoapp.models import Todo
from todoapp.serializers import TodoSerializer,TodoListSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.

class TodoModelViewSetView(ModelViewSet):
    queryset=Todo.objects.all()
    serializer_class=TodoSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)
    lookup_url_kwarg='id'

    def list(self, request, *args, **kwargs):
        user=request.user
        todo=user.todo_set.all()
        serializer=TodoListSerializer(todo,many=True)
        return Response(serializer.data) 
    
    def create(self, request, *args, **kwargs):
        serializer=TodoSerializer(data=request.data)
        user=request.user
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        id=kwargs.get("id")
        user=request.user
        todo=get_object_or_404(Todo,id=id,user=user)
        serializer=TodoListSerializer(todo)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        id=kwargs.get("id")
        user=request.user
        todo=get_object_or_404(Todo,id=id,user=user)
        serializer=TodoListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo.status=serializer._validated_data["status"]
        todo.save()
        return Response(serializer.data)  
    
    def destroy(self, request, *args, **kwargs):
        id=kwargs.get("id")
        user=request.user
        todo=get_object_or_404(Todo,id=id,user=user)
        todo.delete()
        return Response({"message":"todo deleted"})
    
    @action(methods=["get"],detail=True)
    def get_task(self,request,*args,**kwargs):
        id=kwargs.get("id")
        user=request.user
        todo=get_object_or_404(Todo,id=id,user=user)
        task=todo.task
        return Response({"task":task})