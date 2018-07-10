from django.db import models

# Create your models here.
class Member(models.Model):
    username = models.TextField()
    password = models.TextField()
    useremail= models.TextField()
    name= models.TextField()
    userbirth = models.TextField()
    
    class Meta:
        db_table = "members"