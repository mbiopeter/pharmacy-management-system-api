from django.urls import path
from .import users,medicines,invoice

urlpatterns =[
    #user related paths
    path('users/new/', users.newUser, name='newUser'),
    path('users/all/<int:currentUserId>/', users.allUsers, name='allUsers'),
    path('users/profile/<int:id>/', users.updateProfile, name='updateProfile'),
    path('users/details/<int:userId>/', users.profileInfo, name='profileInfo'),
    path('users/permissions/', users.allPermission, name='allPermission'),
    path('users/role/<int:userId>/<int:permissionId>/', users.addRole, name='addRole'),
    path('users/delete/<int:userId>/', users.deleteUser, name='deleteUser'),
    path('users/role/<int:userId>/', users.getPermissions, name='getPermissions'),
    path('users/recycle/restore/<int:userId>/', users.restoreUser, name='getPermissions'),
    path('users/profile/image/<int:id>/', users.uploadImage, name='uploadImage'),
    path('users/roles/name/<int:userId>/', users.roleName, name='roleName'),
    path('users/recycle/all/', users.getRecycledUsers, name='getPermissions'),
    path('users/delete/all/', users.deleteExpired, name='getPermissions'),
    path('users/employeeId/', users.employeeId, name='employeeId'),
    path('login/', users.login, name='login'),
    path('logout/', users.logout, name='logout'),
    #medicine related paths
    path('medicine/add/', medicines.addMedicine, name='addMedicine'),
    path('medicine/all/', medicines.getAll, name='getAll'),
    path('medicine/all/distict/', medicines.distictMed, name='distictMed'),
    path('medicine/count/all/', medicines.medCount, name='medCount'),
    path('medicine/category/all/', medicines.getAllCategory, name='getAllCategory'),
    path('medicine/suppliers/all/', medicines.allSuppliers, name='allSuppliers'),
    path('medicine/supply/lifetime/<int:medId>/', medicines.description, name='description'),
    path('medicine/delete/<int:bId>/', medicines.deleteMed, name='deleteMed'),
    #invoive related paths
    path('invoice/medicine/getall/', invoice.getallMedicine, name='getallMedicine'),
    path('invoice/cart/', invoice.addCart, name='addCart'),
    path('invoice/getCart/<int:sellerId>/', invoice.getCart, name='getCart'),
    path('invoice/getCartAmaunt/<int:sellerId>/', invoice.getcartAmount, name='getcartAmount'),
    path('invoice/delete/<int:batchId>/<int:saleId>/<int:quantity>/', invoice.deleteCart, name='deleteCart'),
]