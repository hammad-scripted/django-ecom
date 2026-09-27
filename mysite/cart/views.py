from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from myapp.models import Product

from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})

@require_POST
def cart_add(request):
    if not request.user.is_authenticated:
        next_url = request.POST.get("next") or reverse("product_list")
        login_url = reverse("login")
        if "application/json" in request.headers.get("Accept", ""):
            return JsonResponse(
                {
                    "status": "authentication_required",
                    "message": "Please sign in before adding items to your bag.",
                    "login_url": f"{login_url}?{urlencode({'next': next_url})}",
                },
                status=401,
            )
        return redirect_to_login(next_url, login_url=login_url)

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
    cart = Cart(request)
    product_id = request.POST.get("product_id", "").strip()
    if not product_id or product_id not in cart.cart:
        messages.error(request, "That item is no longer in your cart. Refresh the page and try again.")
        return redirect("cart_detail")

    try:
        product = Product.objects.get(pk=product_id, active=True)
    except (Product.DoesNotExist, TypeError, ValueError):
        messages.error(request, "This item is no longer available. You can remove it from your cart.")
        return redirect("cart_detail")

    try:
        cart.set_quantity(product, request.POST.get("quantity"))
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
