from unicodedata import name
from django.db import models
# Create your models here.


class FIRM(models.Model):
    Name = models.CharField(max_length=200, null=True)
    Email = models.CharField(max_length=200, null=True)
    HowYouKnowUs = models.CharField(max_length=200, null=True, default='')
    ConnectionStatus = models.CharField(max_length=200, null=True, default='')
    Agree = models.CharField(max_length=200, null=True, default='')

    def __str__(self):
        return self.Name

class Staff(models.Model):
    Name = models.CharField(max_length=200, null=True)
    ID_Number = models.PositiveIntegerField(null=False)
    user = models.ForeignKey(FIRM, null=True, on_delete= models.SET_NULL)

    def __str__(self):
        return self.Name