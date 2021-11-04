from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.products, name='product-list'),
    path("customer/<int:pk>/", views.customers, name="customer-detail"),

    path("create-order/<int:pk>/", views.create_order, name="create-order"),
    path("update-order/<int:pk>/", views.update_order, name="update-order"),
    path("delete-order/<int:pk>/", views.delete_order, name="delete-order"),
]