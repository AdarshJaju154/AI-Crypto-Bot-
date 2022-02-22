from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=200)
    bal = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    def __int__(self):
        return self.bal