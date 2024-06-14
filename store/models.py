from django.db import models
from django.urls import reverse
from Category.models import Category

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    product_slug = models.SlugField(max_length=200, unique=True)
    product_description =   models.CharField(max_length=300,blank=True)
    price               =   models.DecimalField(max_digits=6, decimal_places=2)
    image               =   models.ImageField(upload_to='photos/products',blank=True) 
    quantity            =   models.IntegerField()
    is_available        =   models.BooleanField(default=True)
    category            =   models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date        =   models.DateTimeField(auto_now=True)
    modified_date       =   models.DateTimeField(auto_now=True)
    #on_delete=models.CASCADE -in case we delete the category the product relates with it will be deleted date

    def __str__(self) -> str:
        return self.product_name
    
    def get_product_url(self):
        return reverse('product_details',args=[self.category.slug,self.product_slug])
        
    def get_category_url(self):
        return reverse('product_by_category',args=[self.slug])