from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    # One-to-one relationship between UserProfile and User implemented through OneToOneField
    user = models.OneToOneField(User, related_name='linkedin_user', on_delete=models.CASCADE)
    region = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=11, blank=True)
    detail = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="%Y/%m/%d", blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    profile_created = models.BooleanField(default=False)

class School(models.Model):
    name = models.CharField(max_length=50) 
    location = models.CharField(max_length=50, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class Company(models.Model):
    name = models.CharField(max_length=50) 
    location = models.CharField(max_length=50, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True) 

class UserSchool(models.Model):
    # Many-to-one relationship between UserSchool and UserProfile
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # Many-to-one relationship between UserSchool and School
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    startYear = models.PositiveIntegerField(blank=True, null=True)
    endYear = models.PositiveIntegerField(blank=True, null=True)
    major = models.CharField(max_length=50, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class UserCompany(models.Model):
    # Many-to-one relationship between UserCompany and UserProfile
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # Many-to-one relationship between UserCompany and Company
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
