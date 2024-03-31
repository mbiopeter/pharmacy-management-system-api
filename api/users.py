from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password

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
                api_users(firstName,secondName,email,idNumber,employeeId,gender,username,password)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            """
            param_check = [idNumber]
            params_create = [firstName,secondName,email,idNumber,employeeId,gender,username,hashed_password]
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
def allUsers(request):
    if request.method == 'GET':
        query = """
            SELECT * FROM api_users
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    users_data = []
                    for row in results:
                        user = {
                            'id': row[0],
                            'firstName': row[1],
                            'secondName': row[2],
                            'email': row[3],
                            'employeeId': row[5],
                        }
                        users_data.append(user)
                    return Response(users_data, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'no user found'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            query = """
                SELECT * FROM api_users
                WHERE username = %s
            """
            params = [username]
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    user = cursor.fetchone()
                    if user is not None and check_password(password, user[8]):
                        user_id = user[0]
                        request.session['user_id'] = user_id
                        request.session.set_expiry(3600)                 
                        return Response({'status':True ,'username':username}, status=status.HTTP_200_OK)
                    else:
                        return Response({'status':False }, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def updateProfile(request):
    if request.method == 'POST':
        id = request.data.get('id')
        password = request.data.get('password')
        username = request.data.get('username')
        email = request.data.get('email')
        contact = request.data.get('contact')
        location = request.data.get('location')
        link = request.data.get('link')
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

