from django.db import models
from django.contrib.auth.models import User

class PublicUsers(models.Model):
    user = models.ForeignKey(User , on_delete=models.PROTECT)
    contact = models.IntegerField()
    address = models.CharField(max_length=250)
    date = models.DateField(auto_now=True)
    def __str__(self):
        return "{}".format(self.user)