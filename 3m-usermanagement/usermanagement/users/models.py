from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

# Create your models here.
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,unique=True)
    createdAt = models.DateTimeField()
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='create')
    updatedBy = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name='update')
    updatedAt = models.DateTimeField(null=True,blank=True)
    status = models.BooleanField(default=1)

    def __str__(self):
        return self.user.username
    

class UserRegistration(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=20,unique=True)
    organisation = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    createdAt = models.DateTimeField()
    createdBy = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='_create')
    updatedAt = models.DateTimeField(null=True,blank=True)
    updatedBy = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True,related_name='_update')
    status = models.BooleanField(default=1)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

class Analysis(models.Model):
    feedback = models.CharField(max_length=100)
    image = models.FileField(upload_to='analytics-images')
    time = models.DateTimeField(auto_now_add=True)
    predictionType = models.CharField(max_length=100)
    predictionColor = models.CharField(max_length=100)
    feedbackType = models.CharField(max_length=100)
    feedbackColor = models.CharField(max_length=100)
    location = models.TextField(null=True,blank=True)
    isFlash = models.BooleanField(default=0)
    createdAt = models.DateTimeField()
    createdBy = models.ForeignKey(UserRegistration, on_delete=models.DO_NOTHING,related_name='create')
    updatedAt = models.DateTimeField(null=True, blank=True)
    updatedBy = models.ForeignKey(UserRegistration, on_delete=models.DO_NOTHING,null=True, blank=True,related_name='update')
    status = models.BooleanField(default=1)

    def __str__(self):
        return self.feedback

class MasterLog(models.Model):
    timeStamp = models.DateTimeField()
    activity = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,null=True,blank=True)
    mobileUser = models.ForeignKey(UserRegistration, on_delete=models.DO_NOTHING,null=True,blank=True)
    status = models.BooleanField(default=1)

    def __str__(self):
        return self.activity

class SMSModule(models.Model):
    messageSent = models.IntegerField(default=0)
    allowedMessages = models.IntegerField(default=0)
    isActive = models.BooleanField(default=1)
    status = models.BooleanField(default=1)
    createdAt =	models.DateTimeField()
    updatedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Total messages sent: "+ str(self.messageSent)

class VersionLog(models.Model):
    versionNumber = models.CharField(max_length=10)
    description = models.CharField(max_length=255,null=True, blank=True)
    dateOfRelease = models.DateTimeField()
    askUpgrade = models.BooleanField(default=1)
    status = models.BooleanField(default=1)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField(null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name="createdBy")
    updatedBy = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name="updatedBy",null=True,blank=True)

    def __str__(self):
        return self.versionNumber
    