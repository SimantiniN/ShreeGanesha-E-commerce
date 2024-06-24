from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from carts.models import CartItem,Cart
from carts.views import _cart_id
from .models import Product
from django.db.models import Q #Import Q:handle complex queries with OR conditions.
from Category.models import Category
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.
def store(request,category_slug=None):
    category = None
    products = None
    if category_slug != None:
        category= get_object_or_404(Category,slug=category_slug)
        products = Product.objects.all().filter(category=category,is_available=True).order_by('id')
        paginator =Paginator(products,6)
        page= request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        product_count=products.count()
        paginator = Paginator(products,6)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
    context={
             'products':paged_products,
             'product_count':product_count
             }
    return render(request,'store.html',context)


def product_details(request,category_slug,product_slug):
    # dress_size=[]
    # dress_colors=[]
    try:
        single_product=Product.objects.get(category__slug=category_slug,product_slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        # return HttpResponse(in_cart)
        # exit()
    except Exception as e:
        raise e
    # dress_colors=['Pink','Red','Blue','Yellow','Purple','Black','White']
    # dress_sizes=['S','M','L','XL','XXL']
    context={
             'single_product':single_product,
             'in_cart':in_cart,
            #  'dress_sizes' :dress_sizes,
            #  'dress_colors':dress_colors,
             }
    
    return render(request,'product_details.html',context)
#This part filters products where the related category's slug matches the category_slug.
#product_slug=product_slug: This part filters products where the product's slug matches the product_slug.
# UnorderedObjectListWarning: Pagination may yield inconsistent results with an 
# unordered object_list:<class 'store.models.Product'> QuerySet.
#To avoid this warning we take product by order_by(id)
# products = Product.objects.all().filter(is_available=True).order_by(id)

def search(request):
    if 'keyword' in request.GET:
        keyword= request.GET.get('keyword', '')
        if keyword:
            products = Product.objects.filter(
            Q(product_description__icontains=keyword) | 
            Q(product_name__icontains=keyword)).order_by('-created_date')
            product_count=products.count()
        else:
            products =''
            # products = Product.objects.all().order_by('-created_date')    
            product_count=0;   
    context={
            'products':products,
            'product_count':product_count
    }
    return render(request,'store.html',context)