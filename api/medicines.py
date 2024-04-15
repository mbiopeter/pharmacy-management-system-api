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

def addSupplies(batchId, supplierId, supplierPrice):
    if batchId and supplierId and supplierPrice:
        query = """
            SELECT * FROM api_supplies 
            WHERE batch_id = %s 
            AND supplier_id = %s
        """
        params = [batchId, supplierId]
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchone()
            if results is None:
                query = """
                    INSERT INTO 
                    api_supplies(batch_id, supplier_id, supplierPrice) 
                    VALUES(%s, %s, %s)
                """
                params = [batchId, supplierId, supplierPrice]
                cursor.execute(query, params)
                connection.commit()
                return Response({'message': 'Medicine created successfully.'}, status=status.HTTP_201_CREATED)
            else:
                query = """
                    UPDATE api_supplies 
                    SET supplierPrice = %s
                    WHERE batch_id = %s
                """
                param = [supplierPrice, batchId]
                cursor.execute(query, param)
                connection.commit()
                return Response({'message': 'Medicine successfully updated.'}, status=status.HTTP_200_OK)

def addBatch(quantity, expiry, salePrice, unit, shelf, medId, supplierId, supplierPrice):
    if medId:
        query = """
            SELECT * FROM api_batch 
            WHERE expiry = %s 
            AND medicine_id = %s
        """
        params = [expiry, medId]
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
                addSupplies(batchId, supplierId, supplierPrice)
            else:
                batchId = results[0]
                newQuantity = results[1] + quantity
                batchId = results[0]
                query = """
                    UPDATE api_batch 
                    SET quantity = %s,
                    price = %s 
                    WHERE expiry = %s 
                    AND medicine_id = %s
                """
                params = [newQuantity,salePrice, expiry, medId]
                cursor.execute(query, params)
                connection.commit()
                addSupplies(batchId, supplierId, supplierPrice)

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
        image_data = request.FILES.get('image')  # Retrieve the image data from request
        
        if brandName and genericName and quantity and expiry:
            try:
                if image_data:  # Check if image data is present
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_name = f"{timestamp}_{image_data.name}"
                    image_path = os.path.join('images', image_name)
                    default_storage.save(image_path, image_data)  # Save the image to storage
                    
                    # Update the medicine entry with the image path
                    query = """
                    INSERT INTO 
                    api_medicine(brandName, genericName, description, `usage`, category, image) 
                    VALUES(%s, %s, %s, %s, %s, %s)
                    """
                    params = [brandName, genericName, description, usage, category, image_path]
                else:
                    query = """
                    INSERT INTO 
                    api_medicine(brandName, genericName, description, `usage`, category) 
                    VALUES(%s, %s, %s, %s, %s)
                    """
                    params = [brandName, genericName, description, usage, category]
                    
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    connection.commit()
                    medId = cursor.lastrowid
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
            SELECT m.id,m.genericName,m.category,b.quantity,b.expiry 
            FROM api_medicine as m 
            INNER JOIN api_batch as b 
            ON m.id = b.medicine_id
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    details = []
                    for row in results:
                        detail = {
                            'medicineId': row[0],
                            'name': row[1],
                            'category': row[2],
                            'quantity': row[3],
                            'expiry': row[4],
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
        

def uploadImage(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_data = request.FILES['image']
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_name = f"{timestamp}_{image_data.name}"
            image_path = os.path.join('images', image_name)
            default_storage.save(image_path, image_data)
            
            query = """
            UPDATE api_medicine
            SET image = %s
            WHERE id = (SELECT MAX(id) FROM api_medicine)
            """
            params = [image_path]
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    return Response('Image successfully uploaded', status=status.HTTP_200_OK)
            except Exception as e:
                print(str(e))
                return Response({'error': str(e)}, status=500)
        else:
            return Response('No image found in request', status=status.HTTP_400_BAD_REQUEST)