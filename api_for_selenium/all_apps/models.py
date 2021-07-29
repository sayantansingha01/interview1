from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class OthersField(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=2000)
    phone_number = models.CharField(max_length=2000)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "User grid"
        verbose_name_plural = "User grid"




