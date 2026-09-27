from django.http import JsonResponse
from django.views.decorators.http import require_POST


@require_POST
def cart_add(request):
    if request.method == "POST":
        product_id=request.POST.get('product_id')
        print(f"Product ID: {product_id}")
    return JsonResponse({"status": "success", "message": "Added to cart"})