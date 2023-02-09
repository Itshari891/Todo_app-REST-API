from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns=[
    path('register',views.RegisterAPIView.as_view(),name='signup'),
    path('login',obtain_auth_token,name='signin'),
    path('addtodo',views.TodoAddAPIView.as_view(),name='addtodo'),
    path('listtodo',views.TodoListAPIView.as_view(),name='listtodo'),
    path('todo/<int:id>',views.TodoDetailAPIView.as_view(),name='detail'),
]