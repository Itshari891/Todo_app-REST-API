from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from todoapp.serializers import TodoSerializer,TodoListSerializer
from todoapp.models import Todo
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class TodoAddGenericView(ListCreateAPIView):
    serializer_class=TodoSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        user=self.request.user
        return user.todo_set.all()

class TododetailGenericView(RetrieveUpdateDestroyAPIView):
    serializer_class=TodoListSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
 
    def get_queryset(self):
        user=self.request.user
        return user.todo_set.all()