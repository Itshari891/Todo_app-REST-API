from django.urls import path
from .views import TodoAddGenericView,TododetailGenericView


urlpatterns=[
    path('todo/add',TodoAddGenericView.as_view(),name='add-todo'),
    path('todo/detail/<int:pk>',TododetailGenericView.as_view(),name='detail-todo'),
]