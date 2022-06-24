from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(null=True, max_length=200)
    lastname = models.CharField(null=True, max_length=200)
    phone = models.CharField(null=True, max_length=10)
    username = models.CharField(null=True, max_length=200)
    email = models.EmailField()
    profile_pic = models.FileField(upload_to='static/images/profiles', default='static/images/profiles/img1.jpg')
    staff = models.BooleanField(default=False, null=True)

