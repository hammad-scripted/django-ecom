from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from myapp.models import Product

from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


@require_POST
def cart_add(request):
    product = get_object_or_404(Product, pk=request.POST.get("product_id"), active=True)
    try:
        quantity = int(request.POST.get("product_quantity", "1"))
        cart = Cart(request)
        cart.add(product, quantity)
    except (TypeError, ValueError) as error:
        return JsonResponse({"status": "error", "message": str(error)}, status=400)

    return JsonResponse({"status": "success", "quantity": len(cart)})


@require_POST
def cart_update(request):
    product = get_object_or_404(Product, pk=request.POST.get("product_id"), active=True)
    cart = Cart(request)
    try:
        cart.set_quantity(product, request.POST.get("quantity", "1"))
    except (TypeError, ValueError) as error:
        messages.error(request, str(error))
    else:
        messages.success(request, "Cart updated.")
    return redirect("cart_detail")


@require_POST
def cart_remove(request):
    cart = Cart(request)
    cart.remove(request.POST.get("product_id", ""))
    messages.success(request, "Item removed from your cart.")
    return redirect("cart_detail")
