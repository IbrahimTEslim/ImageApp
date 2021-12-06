from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.related import ForeignKey


# Create your models here.

class User(AbstractUser):
    pass


class Images(models.Model):
    user = ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Alterimages')
    is_deleted = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

