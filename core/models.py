from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    VECHICLE_CHOICE = (
        ('level_1','level_1'),
        ('level_2','level_2'),
        ('level_3','level_3'),
    )
    driver_id = models.CharField(max_length=250,blank=True, null=True)
    profile_pic = models.ImageField(upload_to="images/",blank=True, null=True)
    license_no = models.CharField(max_length=30,blank=True, null=True)
    vehicle_number = models.CharField(max_length=30,blank=True, null=True) 
    vehicle_type = models.CharField(max_length=10,choices=VECHICLE_CHOICE,default='level_1') 
    balance = models.IntegerField()
    
class Transaction(models.Model):
    driver = models.ForeignKey(Driver, on_delete= models.DO_NOTHING, null=True)
    transfered_amount = models.IntegerField()
    date = models.DateTimeField(auto_created=True)
    route = models.CharField(max_length=20, default='Route A')


class Accident(models.Model):
    user = models.ForeignKey(User, on_delete= models.DO_NOTHING)
    date = models.DateTimeField(auto_now=True)
    highlight = models.CharField(max_length=200,blank=True, null=True)
    detail = models.TextField() 
    location = models.CharField(max_length=200,blank=True, null=True)


