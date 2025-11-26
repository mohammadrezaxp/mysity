from django.db import models

class login(models.Model):
    user_name = models.CharField(max_length=20)
    password = models.BooleanField()
