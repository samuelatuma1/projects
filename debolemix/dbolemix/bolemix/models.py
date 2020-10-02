from django.db import models

# Create your models here.

#Each menu item is a list containing all the food contained in each menu
#We also want to give admin the ability to manipulate these tables
#Create yam menu
class Yam(models.Model):
    name = models.CharField(max_length=64)
    descr = models.CharField(max_length=120)
    price = models.IntegerField()
    img = models.ImageField(upload_to='food/imgs/yam', null=True, blank=True)
    

    def __str__(self):
        return f'Name: {self.name}, descr: {self.descr}, Price: {self.price}'

#Create Plantain menu
class Plantain(models.Model):
    name = models.CharField(max_length=64)
    descr = models.CharField(max_length=120)
    price = models.IntegerField()
    img = models.ImageField(upload_to='food/imgs/plantain', null=True, blank=True)

    def __str__(self):
        return f'Name: {self.name}, descr: {self.descr}, Price: {self.price}'


#Create potatoe menu
class Potatoe(models.Model):
    name = models.CharField(max_length=64)
    descr = models.CharField(max_length=120)
    price = models.IntegerField()
    img = models.ImageField(upload_to='food/imgs/potato', null=True, blank=True)

    def __str__(self):
        return f'Name: {self.name}, descr: {self.descr}, Price: {self.price}'

#Admins do not have direct access to this table, as they do the others. However, they can for example, change the status from pending to received.
# Use this to store purchased items
class Purchased(models.Model):
    user = models.CharField(max_length=25, null=True)
    products = models.CharField(max_length=600, null=True)
    total = models.CharField(max_length=6, null=True)
    
    deliverTo = models.CharField(max_length=60, null=True)
    address = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=15, null=True)
    statusValue = models.CharField(max_length=15, null=True)
    time = models.CharField(max_length=100, null=True)
    comment = models.CharField(max_length=150, null=True)
    

    

    def __str__(self):
        return f'User: {self.user}, products: {self.products}, Total: {self.total}, Phone: {self.phone}, status: {self.statusValue}, time: {self.time}'



