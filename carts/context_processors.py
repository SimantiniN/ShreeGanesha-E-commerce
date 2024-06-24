from carts.views import _cart_id
from .models import Cart,CartItem
from django.shortcuts import get_object_or_404
def total_items_in_cart(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            total_quantity=0
            for cart_item in cart_items:
                total_quantity += cart_item.quantity
        except Cart.DoesNotExist:
            total_quantity=0
        return dict(total_quantity=total_quantity)
