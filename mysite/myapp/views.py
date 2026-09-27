# myapp/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product

def product_list(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(active=True)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'myapp/product_list.html', {
        'products': products,
        'query': query,
        'result_count': products.count(),
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    return render(request, 'myapp/product_detail.html', {'product': product})


