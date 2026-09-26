from .views import product_detail, product_list
from django.urls import path

urlpatterns = [
    path("", product_list, name="index"),
    path("<slug:slug>/", product_detail, name="detail"),
]
