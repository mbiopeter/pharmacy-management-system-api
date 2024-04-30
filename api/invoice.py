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
            SELECT b.id, m.genericName, m.image, b.quantity,b.price, b.expiry  
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
                        expiry_date = row[5].strftime('%Y-%m-%d')
                        detail = {
                            'id':row[0],
                            'name':row[1],
                            'img':row[2],
                            'qty':row[3],
                            'price':row[4],
                            'expiry':expiry_date
                        }
                        details.append(detail)
                    return Response(details, status=status.HTTP_200_OK)
                else:
                    return Response({'message':'No medicine found'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            
@api_view(["GET"])
def getCart(request, sellerId):
    if request.method == 'GET':
        query = """
            SELECT s.id, m.genericName, s.quantity,b.id, s.discount,s.price, m.image, s.batch_id
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
                    details = []
                    for row in results:
                        detail = {
                            'id':row[0],
                            'name':row[1],
                            'quantity':row[2],
                            'batchId':row[3],
                            'discount':row[4],
                            'price':row[5],
                            'img':row[6],
                            'batchId':row[7],
                        }
                        details.append(detail)
                    return Response(details, status=status.HTTP_200_OK)
                else:
                    return Response("No items found in cart", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@api_view(['POST'])
def deleteCart(request,batchId,saleId,quantity):
    if request.method == 'POST':

        delete = """
            DELETE FROM api_sales 
            WHERE id = %s
        """
        deleteParam = [saleId]
        update = """
            UPDATE api_batch 
            SET quantity = quantity + %s 
            WHERE id = %s
        """
        updateParams = [quantity,batchId]
        try:
            with connection.cursor() as cursor:
                cursor.execute(update,updateParams)
                cursor.execute(delete,deleteParam)
                return Response({'message':'Item successfully removed from the cart'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)          
        
@api_view(['GET'])
def getcartAmount(request,sellerId):
    if request.method == 'GET':
        query ="""
            SELECT price, discount, quantity
            FROM api_sales             
            WHERE seller_id = %s
            AND status = %s
        """
        params = [sellerId, 'pedding']
        try:
            with connection.cursor() as cursor:
                cursor.execute(query,params)
                results = cursor.fetchall()
                if results:
                    subtotal = 0
                    subdiscount = 0
                    for row in results:
                        subtotal = subtotal + (row[0] * row[2])
                        subdiscount = subdiscount + (row[1] * row[2])
                    total = subtotal - subdiscount
                    details = {
                        'subtotal':subtotal,
                        'subdiscount':subdiscount,
                        'total':total
                    }
                    return Response(details, status=status.HTTP_200_OK)
                else:
                    return Response('unable to calculate the amaunt', status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)          
        

@api_view(['POST'])
def addCart(request):
    if request.method == 'POST':
        sellerId = request.data.get('sellerId')
        quantity = request.data.get('quantity')
        discount = request.data.get('discount')
        batchId = request.data.get('batchId')
        date = datetime.now().strftime("%Y%m%d_%H%M%S")
        if sellerId and quantity and batchId:
            try:
                with connection.cursor() as cursor:
                    query = """
                        SELECT price, quantity FROM api_batch 
                        WHERE id = %s
                    """
                    param = [batchId]
                    updateQuantityQuery = """
                        UPDATE api_batch 
                        SET quantity = quantity - %s 
                        WHERE id = %s
                    """ 
                    updateQuantityParams = [quantity,batchId]
                    addCartQuery = """
                        INSERT INTO 
                        api_sales(date, price, batch_id, seller_id, quantity, discount, status) 
                        VALUES(%s, %s, %s, %s, %s, %s, %s)
                    """
                    checkExistenceQuery = """
                        SELECT * FROM api_sales 
                        WHERE batch_id = %s 
                        AND seller_id = %s 
                        AND status = %s
                    """
                    checkExistenceParams = [batchId, sellerId, 'pedding']
                    #get the price and quantity of the batch
                    cursor.execute(query, param)
                    result = cursor.fetchone()
                    price = result[0]
                    availableQuantity = result[1]

                    addCartParams = [date, price, batchId, sellerId, quantity, discount, 'pedding']
                    #check if the quantity is availble for sale
                    if int(availableQuantity) >= int(quantity):
                        cursor.execute(checkExistenceQuery, checkExistenceParams)
                        rowCount = cursor.rowcount
                        if rowCount >= 1:
                            return Response({'message':'Item already exist in the cart'}, status=status.HTTP_200_OK)
                        else:
                            cursor.execute(updateQuantityQuery, updateQuantityParams)
                            cursor.execute(addCartQuery, addCartParams)
                            return Response({'message':'Item successfully added to the cart'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'massage': 'Quantity not enough to support the transaction'}, status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)  
            except Exception as e:
                print(str(e))
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            
        else:
            return Response('missing requred field', status=status.HTTP_403_FORBIDDEN)
    else:
        return Response('unable to calculate the amaunt', status=status.HTTP_400_BAD_REQUEST)
    