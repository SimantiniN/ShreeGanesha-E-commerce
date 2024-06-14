from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.CharField(max_length=300,blank=True)
    cat_image=models.ImageField(upload_to='photos/categories',blank=True) 
    # blank=True means it is optional

    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories'
     
    def __str__(self) -> str:
        return self.category_name
    
    def get_category_url(self):
        return reverse('product_by_category',args=[self.slug])

# product_by_category' is path name comes from store.url
# urlpatterns = [
#     path('',views.store,name='store'),
#     path('<slug:category_slug>/',views.store,name='product_by_category'),]