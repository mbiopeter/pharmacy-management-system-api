from django.urls import path
from .import users

urlpatterns =[
    path('users/new/', users.newUser, name='newUser'),
    path('users/all/', users.allUsers, name='allUsers'),
    path('users/profile/', users.updateProfile, name='updateProfile'),
    path('users/details/<int:userId>/', users.profileInfo, name='profileInfo'),
    path('users/permissions/', users.allPermission, name='allPermission'),
    path('users/role/<int:userId>/<int:permissionId>/', users.addRole, name='addRole'),
    path('users/role/<int:userId>/', users.getPermissions, name='getPermissions'),
    path('login/', users.login, name='login'),
]