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

#MEDICINE TRANSACTIONS FUNCTIONS     
def addSupplies(batchId, supplierId, supplierPrice, quantity):
    if batchId and supplierId and supplierPrice:
        query = """
            SELECT * FROM api_supplies 
            WHERE batch_id = %s 
            AND supplier_id = %s
        """
        params = [batchId, supplierId]
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchone()
                if results is None:
                    query = """
                        INSERT INTO 
                        api_supplies(batch_id, supplier_id, supplierPrice, quantity) 
                        VALUES(%s, %s, %s, %s)
                    """
                    params = [batchId, supplierId, supplierPrice,quantity]
                    cursor.execute(query, params)
                    connection.commit()
                    return Response({'message': 'Medicine created successfully.'}, status=status.HTTP_201_CREATED)
                else:
                    query = """
                        UPDATE api_supplies 
                        SET supplierPrice = %s,
                        quantity = %s
                        WHERE batch_id = %s
                    """
                    newQuantity = int(results[4]) + int(quantity)
                    param = [supplierPrice,newQuantity, batchId]
                    cursor.execute(query, param)
                    return Response({'message': 'Medicine successfully updated.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def addBatch(quantity, expiry, salePrice, unit, shelf, medId, supplierId, supplierPrice):
    if medId:
        query = """
            SELECT * FROM api_batch 
            WHERE expiry = %s 
            AND medicine_id = %s
        """
        params = [expiry, medId]
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchone()
                if results is None:
                    query = """
                        INSERT INTO 
                        api_batch(quantity, expiry, price, unit, shelf, medicine_id) 
                        VALUES(%s, %s, %s, %s, %s, %s)
                    """
                    params = [quantity, expiry, salePrice, unit, shelf, medId]
                    cursor.execute(query, params)
                    connection.commit()
                    batchId = cursor.lastrowid
                    addSupplies(batchId, supplierId, supplierPrice,quantity)
                else:
                    batchId = results[0]
                    newQuantity = int(results[1]) + int(quantity)
                    query = """
                        UPDATE api_batch 
                        SET quantity = %s,
                        price = %s 
                        WHERE expiry = %s 
                        AND medicine_id = %s
                    """
                    params = [newQuantity,salePrice, expiry, medId]
                    cursor.execute(query, params)
                    addSupplies(batchId, supplierId, supplierPrice, quantity)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
def addMedicine(request):
    if request.method == 'POST':
        brandName = request.data.get('brandName')
        genericName = request.data.get('genericName')
        quantity = request.data.get('quantity')
        expiry = request.data.get('expiry')
        category = request.data.get('category')
        usage = request.data.get('usage')
        shelf = request.data.get('shelf')
        unit = request.data.get('unit')
        description = request.data.get('description')
        salePrice = request.data.get('salePrice')
        supplierPrice = request.data.get('supplierPrice')
        supplierId = request.data.get('supplierId')
        image_data = request.FILES.get('image') 
        
        if brandName and genericName and quantity and expiry:
            try:
                if image_data:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_name = f"{timestamp}_{image_data.name}"
                    image_path = os.path.join('images', image_name)
                    default_storage.save(image_path, image_data) 
                    
                    query = """
                    INSERT INTO 
                    api_medicine(brandName, genericName, description, `usage`, category, image, quantity) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                    """
                    params = [brandName, genericName, description, usage, category, image_path, quantity]
                else:
                    query = """
                    INSERT INTO 
                    api_medicine(brandName, genericName, description, `usage`, category, quantity) 
                    VALUES(%s, %s, %s, %s, %s)
                    """
                    params = [brandName, genericName, description, usage, category, quantity]
                check = """
                    SELECT * FROM api_medicine 
                    WHERE brandName =%s 
                    AND genericName =%s 
                    AND category =%s
                """
                update = """
                    UPDATE api_medicine 
                    SET quantity =%s 
                    WHERE id =%s
                """
                checkParams = [brandName, genericName, category]    
                with connection.cursor() as cursor:
                    cursor.execute(check, checkParams)
                    results = cursor.fetchone()
                    if results is None:
                        cursor.execute(query, params)
                        connection.commit()
                        medId = cursor.lastrowid
                        addBatch(quantity, expiry, salePrice, unit, shelf, medId, supplierId, supplierPrice)
                    else:
                        medId = results[0]
                        newQuantity = int(results[7]) + int(quantity)
                        updateParams = [newQuantity, medId]
                        cursor.execute(update, updateParams)
                        addBatch(quantity, expiry, salePrice, unit, shelf, medId, supplierId, supplierPrice)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message': 'Medicine added successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def getAll(request):
    if request.method == 'GET':
        query = """
            SELECT b.id,m.genericName,m.brandName,m.category,b.quantity,b.expiry 
            FROM api_medicine as m 
            RIGHT JOIN api_batch as b 
            ON m.id = b.medicine_id
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
                            'batchId': row[0],
                            'name': row[1],
                            'brandName':row[2],
                            'category': row[3],
                            'quantity': row[4],
                            'expiry':expiry_date,
                        }
                        details.append(detail)
                    return Response(details, status=status.HTTP_200_OK)
                else:
                    return Response({'message':'No medicine found'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getAllCategory(request):
    if request.method =='GET':
        query = """
            SELECT DISTINCT category FROM api_medicine;
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    categories = []
                    for row in results:
                        category = {
                            'name':row[0]
                        }
                        categories.append(category)
                    return Response(categories, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
def medCount(request):
    if request.method == 'GET':
        query = """
            SELECT COUNT(DISTINCT genericName) AS count FROM api_medicine
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchone()
                if row:
                    count = row[0]
                    result = {'count': count}
                    return Response(result, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET', 'POST'])
def allSuppliers(request):
    if request.method == 'GET':
        query ="""
            SELECT * FROM api_supplier
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    suppliers = []
                    for row in results:
                        supplier = {
                            'id':row[0],
                            'name':row[1]
                        }
                        suppliers.append(supplier)
                    return Response(suppliers, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
def distictMed(request):
    if request.method == 'GET':
        query = """
            SELECT DISTINCT id, brandName, GenericName
            FROM api_medicine
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    details = []
                    for row in results:
                        detail = {
                            'Id': row[0],
                            'brandName':row[1],
                            'name': row[2],
                        }
                        details.append(detail)
                    return Response(details, status=status.HTTP_200_OK)
                else:
                    return Response({'message':'No medicine found'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#MEDICINE DESCRIPTION FUNCTIONS

@api_view(['GET', 'POST'])
def description(request, medId):
    if request.method == 'GET':
        query = """
            SELECT m.id, m.quantity, m.description, m.usage, b.quantity ,m.genericName
            FROM api_medicine AS m 
            LEFT JOIN api_batch AS b 
            ON m.id = b.medicine_id 
            WHERE b.id = %s
        """
        param = [medId]
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, param)
                result = cursor.fetchone()
                details = {
                    'id': result[0],
                    'lifetimeSupply':result[1],
                    'description':result[2],
                    'usage':result[3],
                    'stockLeft':result[4],
                    'name':result[5]
                }
                if result:                  
                    return Response(details, status=status.HTTP_200_OK) 
                else:
                    return Response({'message':'No medicine found'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def deleteMed(request, bId):
    if request.method == 'POST':
        check = """
            SELECT quantity 
            FROM  api_batch 
            WHERE id = %s
        """
        deleteBatch = """
            DELETE FROM api_batch 
            WHERE id = %s
        """
        deleteSupplies = """
            DELETE FROM api_supplies 
            WHERE batch_id = %s
        """
        param = [bId]
        try:
            with connection.cursor() as cursor:
                cursor.execute(check, param)
                result = cursor.fetchone()
                if result is not None:
                    quantity = result[0]
                    if quantity > 0:
                        return Response({'message':'Medicine is still in stock'}, status=status.HTTP_200_OK)
                    else:
                        cursor.execute(deleteSupplies,param)
                        cursor.execute(deleteBatch, param)
                        return Response({'message':'Medicine is successfully deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)