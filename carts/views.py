from django.shortcuts import render,redirect,get_object_or_404
from carts.models import Cart,CartItem
from store.models import Product,Variation
from django.http import HttpResponse
from decimal import Decimal

# Create your views here.
def _cart_id(request): # PEP8 is private functon so _functionaname
    cart=request.session.session_key #this function is used to create or get session key 
    if not cart:
        cart= request.session.create()
    return cart

def add_cart(request,product_id): # add_product_to_the_cart
    product=Product.objects.get(id=product_id)
    print(product.quantity)
    product_variations=[]
    if request.method == 'POST':
        for item in request.POST:
            key= item
            value=request.POST[key]
            try:
                variation = Variation.objects.filter(product=product,variation_category__iexact=key, variation_value__iexact=value)
                product_variations.append(variation)
            except Variation.DoesNotExist:
                pass
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request)) # from def _cart_id(request)
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
                                    cart_id =_cart_id(request)
                                )        
    cart.save()
    is_cart_item_exist = CartItem.objects.filter(cart=cart, product=product)
    
    if is_cart_item_exist: #and cart_item.quantity < product.quantity:
        cart_item = CartItem.objects.filter(cart=cart, product=product)
        existing_variations_list =[]
        cart_item_id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_variations_list.append(list(existing_variation))
            cart_item_id.append(item.id)
 #Querset is list  within list so list(existing_variation)
 # [[<QuerySet [<Variation: Blue>, <Variation: Medium>]>, <QuerySet [<Variation: Blue>, <Variation: Small>]>,
 #  <QuerySet [<Variation: Pink>, <Variation: Large>]>, <QuerySet [<Variation: Blue>, <Variation: Medium>]>,
 #  <QuerySet []>, <QuerySet []>]
        # print(existing_variations_list)
        if product_variations in existing_variations_list:
             existing_variations_list_index = existing_variations_list.index(product_variations)
             item_id=cart_item_id[existing_variations_list_index]
             #  print(existing_variations_list_index) =4
            #  print(item_id)
             item=CartItem.objects.get(product=product,id=item_id)
             item.quantity += 1
             item.save()
        else:
            item= CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
            )
            if len(product_variations)>0:
                item.variations.clear()
                item.variations.add(*product_variations)
            item.quantity += 1
            item.save()
    else:
        cart_item= CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
            )
        if len(product_variations)>0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variations)
        cart_item.save()
    # return HttpResponse(cart_item.variations)
    #return HttpResponse(cart_item.product)
    # exit()
    return redirect('cart')

def  remove_cart(request,product_id,cart_item_id):
    product=Product.objects.get(id=product_id)
    cart=get_object_or_404(Cart,cart_id=_cart_id(request)) # from def _cart_id(request)     
    cart.save()
    # try:
    cart_item=get_object_or_404(CartItem,cart=cart,product=product,id=cart_item_id) 
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    # except CartItem.DoesNotExist:
    #     pass

    return redirect('cart')

def remove_entire_cartitem(request,product_id,cart_item_id):
    product=Product.objects.get(id=product_id)
    cart=get_object_or_404(Cart,cart_id=_cart_id(request)) # from def _cart_id(request)     
    cart.save()
    cart_item=CartItem.objects.get(cart=cart,product=product,id=cart_item_id)  
    cart_item.delete()
    return redirect('cart')

def cart(request,total_price=0,cart_items=None,quantity=0,GST=0,total_quantity=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
    except CartItem.DoesNotExist:
        pass    
    for cart_item in cart_items:
        total_price += cart_item.product.price * cart_item.quantity
        # quantity = cart_item.quantity
        total_quantity +=cart_item.quantity
        # print(total_quantity)
    GST= round((total_price * Decimal('1.1'))/100,2)
    grant_total = total_price + GST
    context={
        'quantity':quantity,
        'total_price':total_price,
        'cart_items':cart_items,
        'GST':GST,
        'grant_total' :grant_total ,
        # 'total_quantity':total_quantity,
    }
    return render(request,'cart.html',context)
