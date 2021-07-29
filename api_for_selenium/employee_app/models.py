from django.db import models

# Create your models here.

class EmpModels(models.Model):
    emp_name = models.CharField(max_length=2000)
    emp_designation = models.CharField(max_length=2000)
    address = models.CharField(max_length=2000)
    city = models.CharField(max_length=2000)
    mobile = models.CharField(max_length=100)


    def __str__(self):
        return self.emp_id