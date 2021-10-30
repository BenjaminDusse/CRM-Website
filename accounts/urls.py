from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.products, name='product-list'),
    path("customers/", views.customers, name="customers-list")
]