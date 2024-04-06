from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

@api_view(['POST'])
def newUser(request):
    if request.method  == 'POST':
        firstName = request.data.get('firstName')
        secondName = request.data.get('secondName')
        email = request.data.get('email')
        idNumber = request.data.get('idNumber')
        employeeId = request.data.get('employeeId')
        gender = request.data.get('gender')
        username = request.data.get('username')
        password = request.data.get('password')
        if firstName and secondName and email and idNumber and employeeId and username and password:
            hashed_password = make_password(password)
            query_check = """
                SELECT * FROM api_users
                WHERE idNumber = %s
            """
            query_create = """
                INSERT INTO 
                api_users(firstName,secondName,email,idNumber,employeeId,gender,username,password,status)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            param_check = [idNumber]
            params_create = [firstName,secondName,email,idNumber,employeeId,gender,username,hashed_password,'Active']
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query_check,param_check)
                    results = cursor.fetchone()
                    if results is None:
                        cursor.execute(query_create, params_create)
                        return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'error': 'User with the provided ID already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def allUsers(request,currentUserId):
    if request.method == 'GET':
        if currentUserId is not None:
            query = """
                SELECT * 
                FROM api_users  
                WHERE status = %s AND id != %s
            """
            params = ['Active',currentUserId]
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query,params)
                    results = cursor.fetchall()
                    if results:
                        users_data = []
                        for row in results:
                            fullName = row[1] + ' ' + row[2]
                            user = {
                                'id': row[0],
                                'fullName': fullName,
                                'email': row[3],
                                'employeeId': row[5],
                            }
                            users_data.append(user)
                        return Response(users_data, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'no user found'}, status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'You are not looged in'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            query = """
                SELECT * FROM api_users
                WHERE username = %s AND status = %s
            """
            params = [username, 'Active']
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    user = cursor.fetchone()
                    if user is not None and check_password(password, user[8]):
                        user_id = user[0]
                        request.session['user_id'] = user_id
                        request.session.set_expiry(60*60*2) 
                        print("Session Data:", request.session)
                        return JsonResponse({'status': True, 'user_id': user_id, 'username': username})
                    else:
                        print('login unsuccessful')
                        return JsonResponse({'status': False}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        try:
            request.session.flush()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def updateProfile(request,id):
    if request.method == 'POST':
        password = request.data.get('password')
        username = request.data.get('username')
        email = request.data.get('email')
        contact = request.data.get('contact')
        location = request.data.get('location')
        link = request.data.get('link')
        try:
            if password:
                hashed_password = make_password(password)
                query = """
                    UPDATE api_users SET password = %s WHERE id = %s
                """
                params = [hashed_password,id]
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                return Response({'status':'user informations updated succesfully'}, status=status.HTTP_200_OK)
            if username:
                query = """
                    UPDATE api_users SET username = %s WHERE id = %s
                """
                params = [username,id]
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                return Response({'status':'user informations updated succesfully'}, status=status.HTTP_200_OK)
            if email:
                query = """
                    UPDATE api_users SET email = %s WHERE id = %s
                """
                params = [email,id]
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                return Response({'status':'user informations updated succesfully'}, status=status.HTTP_200_OK)
            if contact:
                query = """
                    UPDATE api_users SET contact = %s WHERE id = %s
                """
                params = [contact,id]
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                return Response({'status':'user informations updated succesfully'}, status=status.HTTP_200_OK)
            if location:
                query = """
                    UPDATE api_users SET location = %s WHERE id = %s
                """
                params = [location,id]
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                return Response({'status':'user informations updated succesfully'}, status=status.HTTP_200_OK)
            if link:
                query = """
                    UPDATE api_users SET link = %s WHERE id = %s
                """
                params = [link,id]
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                return Response({'status':'user informations updated succesfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def profileInfo(request, userId):
    if request.method == 'GET':
        if userId:
            query = """
                SELECT firstName, secondName,email, location, link,img 
                FROM api_users 
                WHERE id = %s
            """
            param = [userId]
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query,param)
                    result = cursor.fetchone()
                if result:
                    user = {
                        'firstName': result[0],
                        'secondName': result[1],
                        'email': result[2],
                        'location': result[3],
                        'link': result[4],
                        'img': result[5],
                    }
                    return Response(user, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'user not found'}, status=status.HTTP_204_NO_CONTENT) 
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'User Id is not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def allPermission(request):
    if request.method == 'GET':
        query = """
            SELECT * FROM api_permissions;
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
            if results:
                permissions = []
                for row in results:
                    permission = {
                        'id': row[0],
                        'name': row[1]
                    }
                    permissions.append(permission)
                return Response(permissions, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'no permission found'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
def addRole(request,userId,permissionId):
    if request.method == 'POST':
        if userId and permissionId:
            querycheck = """
                SELECT * FROM 
                api_roles WHERE
                user_id = %s AND
                permission_id = %s
            """
            queryadd = """
                INSERT INTO 
                api_roles(user_id, permission_id)
                VALUES (%s, %s)
            """
            params = [userId, permissionId]
            try:
                with connection.cursor() as cursor:
                    cursor.execute(querycheck, params)
                    results = cursor.fetchall()
                    if results is None:
                        cursor.execute(queryadd, params)
                    else:
                        return Response({'error': 'Permission allready assigned to the user'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'UserId or permissionId is not provided'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getPermissions(request,userId):
    if request.method == 'GET':
        if userId:
            query = """
                SELECT p.* FROM
                api_permissions AS p 
                INNER JOIN api_roles AS r 
                ON p.id = r.permission_id 
                WHERE r.user_id = %s
            """
            param = [userId]
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, param)
                    results = cursor.fetchall()
                    if results:
                        user_roles = []
                        for row in results:
                            role = {
                                'id':row[0],
                                'name':row[1]
                            }
                            user_roles.append(role)
                        return Response(user_roles, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'UserId is not provided'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
def deleteUser(request, userId):
    if request.method == 'POST':   
        if userId:    
            query = """
                UPDATE api_users 
                SET status = %s 
                WHERE id = %s
            """
            params = ['Deleted',userId]
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query,params)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'UserId is not provided'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message': 'user deleted successfully.'}, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
def DeleteUserBin(request,userId):
    if request.method == 'POST':
        if userId:
            roleQuery = """
                DELETE FROM api_roles WHERE user_id = %s
            """
            param = [userId]
            try:
                with connection.cursor() as cursor:
                    cursor.execute(roleQuery,param)
                    queryUser = """
                        DELETE FROM api_users WHERE id = %s AND status = 'Deleted'
                    """
                    cursor.execute(queryUser, param)
                    return Response('User deleted successfully', status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'UserId is not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def restoreUser(request, userId):
    if request.method == 'POST':
        if userId:
            query = """
                UPDATE api_users SET status = %s WHERE id = %s
            """
            params = ['Active',userId]
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    return Response('User successfully restored', status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'UserId is not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GEt'])
def getRecycledUsers(request):
    if request.method == 'GET':
        query = """
            SELECT * FROM api_users WHERE status = %s
        """
        param = ['Deleted']
        try:
            with connection.cursor() as cursor:
                cursor.execute(query,param)
                results = cursor.fetchall()
                if results is not None:
                    users_data = []
                    for row in results:
                        fullName = row[1] + ' ' + row[2]
                        user = {
                            'id': row[0],
                            'fullName': fullName,
                            'email': row[3],
                            'employeeId': row[5],
                        }
                        users_data.append(user)
                    return Response(users_data, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'no user found'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)