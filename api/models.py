from django.db import models
# USER RELATED TABLES
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
    img = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.employeeId
    
class permissions(models.Model):
    permission =  models.CharField(max_length=200,null=False,blank=False)
    def __str__(self):
        return self.userId
    
class roles(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    permission = models.ForeignKey(permissions, on_delete=models.CASCADE)
    def __str__(self):
        return self.userId
    
#MEDICINE RELATED TABLES
class medicine(models.Model):
    brandName = models.CharField(max_length=200,null=False,blank=False)
    genericName = models.CharField(max_length=200,null=False,blank=False)
    description = models.TextField()
    usage = models.TextField()
    category = models.CharField(max_length=200,null=False,blank=False)
    image = models.CharField(max_length=200,null=False,blank=False)
    def __str__(self):
        return self.genericName
    
class batch(models.Model):
    medicineId = models.ForeignKey(medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    expiery = models.DateTimeField()
    price = models.IntegerField(null=True)
    supplierPrice = models.IntegerField(null=True)
    supplier = models.CharField(max_length=200,null=True,blank=True)
    unit = models.CharField(max_length=200,null=True,blank=True)
    shelf = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.medicineId
    
class sales(models.Model):
    batchId = models.ForeignKey(batch, on_delete=models.CASCADE)
    date = models.DateTimeField(max_length=10,null=True,blank=True)
    price = models.IntegerField(null=False)
    salerId =  models.ForeignKey(users, on_delete=models.CASCADE)
    def __str__(self):
        return self.medicineId

class supplier(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False)
    address = models.CharField(max_length=200,null=True,blank=True)