from django.urls import path
from .import users

urlpatterns =[
    path('users/new/', users.newUser, name='newUser'),
    path('users/all/', users.allUsers, name='allUsers'),
]