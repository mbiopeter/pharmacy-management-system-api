from django.db import models

# Create your models here.
class Medicine(models.Model):
    brandName = models.CharField(max_length=300,null=False,blank=False)
    genericName = models.CharField(max_length=300,null=False,blank=False)
    quantity = models.IntegerField()
    expieryDate = models.DateField()
    category = models.CharField(max_length=300,null=True,blank=True)
    shelfNo = models.CharField(max_length=300,null=True,blank=True)
    unit = models.CharField(max_length=300,null=False,blank=False)
    group = models.CharField(max_length=300,null=True,blank=True)
    tax = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
    supplierPrice = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
    salePrice = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
    supplier = models.CharField(max_length=200,null=True,blank=True)
    howToUse = models.TextField()
    sideEffects = models.TextField()
    image = models.CharField(max_length=300,null=True,blank=True)
    def __str__(self):
        return self.brandName
    
class generalMedicine(models.Model):
    medicineId = models.IntegerField()
    quantity =  models.IntegerField()
    def __str__(self):
        return self.medicineId

class users(models.Model):
    firstName = models.CharField(max_length=200,null=False,blank=False)
    secondName = models.CharField(max_length=200,null=False,blank=False)
    email = models.CharField(max_length=200,null=False,blank=False)
    idNumber = models.IntegerField()
    employeeId = models.CharField(max_length=200,null=False,blank=False)
    gender = models.CharField(max_length=200,null=True,blank=True)
    username = models.CharField(max_length=200,null=False,blank=False)
    password = models.CharField(max_length=600,null=False,blank=False)
    contact = models.IntegerField(null=True)
    location = models.CharField(max_length=200,null=True,blank=True)
    link = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.employeeId