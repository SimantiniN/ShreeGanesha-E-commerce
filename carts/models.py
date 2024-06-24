from django.db import models
from django.urls import reverse
from store.models import Product,Variation

# Create your models here.
class Cart(models.Model):
        cart_id=models.CharField(max_length=250,blank=True)
        date_added=models.DateTimeField(auto_now_add=True)

def __str__(self)-> str:
        return self.cart_id

class CartItem(models.Model):
        product=models.ForeignKey(Product,on_delete=models.CASCADE)
        variations=models.ManyToManyField(Variation,blank=True) # 1 product has many variations like pink-large,pink medium,red-extralarge etc
        cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
        quantity=models.IntegerField()
        is_active=models.BooleanField(default=True)
        
        def sub_total(self):
                return self.product.price * self.quantity

        class Meta:
                verbose_name = 'CartItem'
                verbose_name_plural = 'CartItems'

def __str__(self)-> str:
        return self.product