from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    reg = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_no = models.BigIntegerField()
    email = models.EmailField(default='')
    age = models.BigIntegerField()

    def __str__(self):
        return f"{self.reg} - {self.contact_no}" 
    
class History(models.Model):
    id = models.AutoField(primary_key=True)
    reg = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.TextField(default=' ')

    def __str__(self):
        return f"{self.id} - {self.reg}"
