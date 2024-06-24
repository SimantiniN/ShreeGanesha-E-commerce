
from django.urls import path
from .import views


urlpatterns = [
    path('',views.store,name='store'),
    path('category/<slug:category_slug>/',views.store,name='product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>',views.product_details,name='product_details'),
    path('search/', views.search, name='search'),
]  
#<slug:category_slug>/: 
# This part of the path defines a URL pattern that includes a slug parameter named category_slug. 
# The slug: converter ensures that the captured value will match a slug format, 
# which typically consists of letters, numbers, hyphens, and underscores. 
# In this context, a slug is usually a URL-friendly version of a string,
#  often used to represent categories, articles, or products in a readable and SEO-friendly manner.
#path('search/', views.search, name='search'), is consider as category
# as we already write path('<slug:category_slug>/',views.store,name='product_by_category'),