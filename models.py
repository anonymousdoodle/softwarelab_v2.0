from django.db import models
from django.contrib import admin

#adfs is the database model name for the users (students) who are registered
class adfs(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.TextField()    
    email = models.TextField()
    password = models.TextField()

    def __str__(self):
        return self.username


#teacher model for editing teacher cards
class teachers(models.Model):
    #let the fields stay for user verification

    #for managing content such as ID, IMAGE, NAME, AND CARD (WORK IN PROGRESSS)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='teacher_images/', null=True, blank=True)



#for admin user management
class AdminUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.TextField()
    password = models.TextField()
    

    def __str__(self):
        return self.username
    



