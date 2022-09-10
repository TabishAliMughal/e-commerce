from distutils.sysconfig import customize_compiler
from django.db import models


class Categories(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank = True, null=True)
    name = models.CharField(max_length = 50)
    slug = models.SlugField(max_length=200)
    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"
    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])  

class Products(models.Model):
    name = models.CharField(max_length = 50)
    picture = models.URLField()
    category = models.ForeignKey(Categories , on_delete = models.PROTECT)
    price = models.IntegerField()
    available = models.BooleanField()
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    contact = models.IntegerField()
    total_price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.customer

class OrderProducts(models.Model):
    order = models.ForeignKey(Order , on_delete=models.PROTECT)
    product = models.ForeignKey(Products , on_delete=models.PROTECT)
    qty = models.IntegerField()
    unit_price = models.IntegerField()
    def __str__(self):
        return "{}".format(self.order)