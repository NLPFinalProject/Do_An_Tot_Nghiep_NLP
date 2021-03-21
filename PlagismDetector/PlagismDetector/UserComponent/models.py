from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, blank=False, default='',primary_key=True)
    password = models.CharField(max_length=100, blank=False, default='')
    name = models.CharField(max_length=30, blank=False, default='')
    EmailOrganization = models.CharField(max_length=30,blank=True, default='')
    DateOfBirth = models.DateTimeField(blank=True)
    active = models.BooleanField(default=False,blank=False)
    phone = models.CharField(max_length=15,blank=True,  default='')
    def __str__(self):
        return self.username
    class Meta:
        db_table='user'