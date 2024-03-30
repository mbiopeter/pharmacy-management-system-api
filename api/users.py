from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection
from rest_framework import status
from django.contrib.auth.hashers import make_password

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