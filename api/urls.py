from django.urls import path
from .import users,medicines

urlpatterns =[
    #user related paths
    path('users/new/', users.newUser, name='newUser'),
    path('users/all/', users.allUsers, name='allUsers'),
    path('users/profile/<int:id>', users.updateProfile, name='updateProfile'),
    path('users/details/<int:userId>/', users.profileInfo, name='profileInfo'),
    path('users/permissions/', users.allPermission, name='allPermission'),
    path('users/role/<int:userId>/<int:permissionId>/', users.addRole, name='addRole'),
    path('users/delete/<int:userId>/', users.deleteUser, name='deleteUser'),
    path('users/role/<int:userId>/', users.getPermissions, name='getPermissions'),
    path('login/', users.login, name='login'),
    path('logout/', users.logout, name='logout'),
    #medicine related paths
    path('medicine/add/', medicines.addMedicine, name='addMedicine'),
    path('medicine/all/', medicines.getAll, name='getAll'),
]