from django.db import models

class Sign_Up(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    password = models.BooleanField()
    email = models.EmailField()
    phon_number =models.IntegerField()
    birthday = models.DateTimeField(auto_now= True)