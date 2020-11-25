from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    # One-to-one relationship between UserProfile and User implemented through OneToOneField
    user = models.OneToOneField(User, related_name='linkedin_user', on_delete=models.CASCADE)
    region = models.CharField(max_length=50)
    contact = models.CharField(max_length=11)
    # photo 

class School(models.Model):
    name = models.CharField(max_length=50) 
    location = models.CharField(max_length=50)

class Company(models.Model):
    # One-to-many relationship between UserCompany and Company
    name = models.CharField(max_length=50) 
    location = models.CharField(max_length=50)

class UserSchool(models.Model):
    # Many-to-one relationship between UserSchool and UserProfile
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    startYear = models.PositiveIntegerField()
    endYear = models.PositiveIntegerField()
    major = models.CharField(max_length=50, blank=True)

class UserCompany(models.Model):
    # Many-to-one relationship between UserCompany and UserProfile
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
