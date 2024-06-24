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

# Custom Manager info down
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)



variation_category_choice=(
    ('color','color'),
    ('size','size')
)
#The first element is the value that will be stored in the database.
#The second element is the human-readable name 
#that will be displayed in forms and the Django admin interface.
class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=50,choices=variation_category_choice)
    variation_value =models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

# inform class Variation that we create VariationManager module so we register here
    objects=VariationManager()  

    def __str__(self) -> str:
        return self.variation_value
# def __str__(self) -> str __str take by new version: instead def __unicode__(self) old version will take __unicode_
    # def __unicode__(self) -> str:
    #     return self.product when we post the variation it retuens the objcet so we use def __str__(self) like folllowing
    
#Default Manager
#The default manager is accessible via the objects attribute on the model class. 
# It allows you to perform common database operations like all(), filter(), get(), exclude(), etc.
# Default Manager: Django provides a default manager named objects for every model class, 
                    # used to perform standard query operations.
                    # here {% for color in single_product.variation_set.all %}
                    #variation_set.all is default operation

# Custom Manager: You can define custom managers to add additional methods or 
                    # to modify the default behavior of the queryset.
                    #here {% for color in single_product.variation_set.colors%}
                    #variation_set.colors is custom operation

# Implementation: Custom managers are implemented by subclassing models.
                    # Manager and adding them to the model.