from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection
from rest_framework import status
from django.http import JsonResponse

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
        image = request.data.get('image')
        salePrice = request.data.get('salePrice')
        supplierPrice = request.data.get('supplierPrice')
        supplierId = request.data.get('supplierId')
        if brandName and genericName and quantity and expiry:
            try:
                checkMed = """
                    SELECT * FROM api_medicine 
                    WHERE brandName = %s 
                    AND genericName = %s
                """
                checkParams = [brandName, genericName]
                with connection.cursor() as cursor:
                    cursor.execute(checkMed, checkParams)
                    results = cursor.fetchone()
                    if results is None:
                        query = """
                            INSERT INTO 
                            api_medicine(brandName, genericName, description, `usage`, category, image) 
                            VALUES(%s, %s, %s, %s, %s, %s)
                        """
                        params = [brandName, genericName, description, usage, category, image]
                        cursor.execute(query, params)
                        connection.commit()
                        medId = cursor.lastrowid
                        addBatch(quantity, expiry, salePrice, unit, shelf, medId, supplierId, supplierPrice)
                    else:
                        medId = results[0]
                        query = """
                            UPDATE api_medicine
                            SET description = %s,
                            `usage` = %s, 
                            image = %s
                            WHERE id = %s
                        """
                        params = [description, usage, image, medId]
                        cursor.execute(query, params)
                        connection.commit()
                        addBatch(quantity, expiry, salePrice, unit, shelf, medId, supplierId, supplierPrice)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message': 'Medicine added successfully.'}, status=status.HTTP_201_CREATED)
