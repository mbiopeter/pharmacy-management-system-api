from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection
from rest_framework import status
from django.http import JsonResponse
from datetime import datetime
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import transaction


@api_view(['GET'])
def getallMedicine(request):
    if request.method == 'GET':
        query = """
            SELECT b.id, m.genericName, m.image, b.quantity, b.expiry  
            FROM api_batch AS b 
            LEFT JOIN api_medicine AS m 
            ON m.id = b.medicine_id 
            ORDER BY b.expiry ASC;
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    details = []
                    for row in results:
                        detail = {
                            'id':row[0],
                            'name':row[1],
                            'img':row[2],
                            'qty':row[3],
                            'expiry':row[4]
                        }
                        details.append(detail)
                    return Response(details, status=status.HTTP_200_OK)
                else:
                    return Response({'message':'No medicine found'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            
@api_view(["POST"])
def addCart(request):
    if request.method == 'POST':
        batchId = request.data.get('batchId')
        price = request.data.get('price')
        discount = request.data.get('discount')
        quantity = request.data.get('quantity')
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        sellerId = request.data.get('sellerId')
        if batchId is None:
            return Response({'error': "Batch ID cannot be null"}, status=status.HTTP_400_BAD_REQUEST)
        queryCheck = """
            SELECT * FROM api_sales 
            WHERE batch_id = %s 
            AND seller_id = %s
        """
        checkParams = [batchId, sellerId]
        queryAdd = """
            INSERT INTO 
            api_sales(date, price, batch_id, seller_id, quantity, phone, discount, email, name, status) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        queryAddParams = [timestamp, price, batchId, sellerId, quantity, phone, discount, email, name, 'Pedding']
        queryUpdate = """
            UPDATE api_sales 
            SET quantity = %s, 
            price = %s, 
            discount = %s 
            WHERE batch_id = %s 
            AND seller_id = %s 
            AND status = %s
        """
        queryUpdateParams = [quantity, price, discount, batchId, sellerId, 'pedding']
        try:
            with connection.cursor() as cursor:
                cursor.execute(queryCheck, checkParams)
                results = cursor.fetchone()
                if results is not None:
                    cursor.execute(queryUpdate, queryUpdateParams)
                    return Response({'Message':'Medicine Cart Successfully update'}, status=status.HTTP_200_OK)
                else:
                    cursor.execute(queryAdd, queryAddParams)
                    return Response({'Message':'Medicine Successfully added to cart'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(["GET"])
def getCart(request, sellerId):
    if request.method == 'GET':
        query = """
            SELECT s.id, m.genericName, s.quantity
            FROM api_medicine m
            INNER JOIN api_batch b ON m.id = b.medicine_id
            INNER JOIN api_sales s ON b.id = s.batch_id
            WHERE s.seller_id = %s
            AND s.status = %s
        """
        params = [sellerId, 'pedding']
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                if results:
                    medicine_quantities = {}
                    medicine_id = 0
                    for row in results:
                        medicine_id = medicine_id + 1
                        medicine_name = row[1]
                        quantity = row[2]
                        
                        if medicine_name in medicine_quantities:
                            medicine_quantities[medicine_name] += quantity
                        else:
                            medicine_quantities[medicine_name] = quantity
                    
                    details = [{'id':medicine_id,'name': name, 'quantity': quantity} for name, quantity in medicine_quantities.items()]                   
                    return Response(details, status=status.HTTP_200_OK)
                else:
                    return Response("No items found in cart", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     