from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .cart import Cart
from myapp.models import Product
from django.shortcuts import get_object_or_404


@require_POST
def cart_add(request):
    # cart instance
    cart=Cart(request)
    if request.method == "POST":
        product_id=request.POST.get('product_id')
        product_quantity=request.POST.get('product_quantity')
        product=get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_quantity)
        cart_len=cart.__len__()
        
        
    return JsonResponse({"status": "success", "quantity": cart_len})

