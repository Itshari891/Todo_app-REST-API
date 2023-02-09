from rest_framework import serializers
from django.contrib.auth import get_user_model
User=get_user_model()
from rest_framework.response import Response
from .models import Todo

class UserSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True,required=True)
    class Meta:
        model=User
        fields=[
            "username",
            "email",
            "password",
            "password2",
        ]
        extra_kwargs={
            "email":{"required":True}
        }

    def save(self, **kwargs):
        account=User(
            username=self.validated_data["username"],
            email=self.validated_data["email"]
        )
        password=self.validated_data["password"]
        password2=self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password":"not matching"})
        account.set_password(password)
        account.save()
        return account

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields=[
            "id",
            "task",
            "created_date",
            "status",
            "user"
        ]
        extra_kwargs={
            "task":{"required":True},
            "user":{"read_only":True}
        }

class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields=[
            "id",
            "task",
            "status",
            "created_date",
        ]
        extra_kwargs={
            "task":{"read_only":True}
        }