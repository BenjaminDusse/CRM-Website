from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.products, name='product-list'),
    path("customers/<int:pk>/", views.customers, name="customers-list"),


    path("create-order/", views.create_order, name="create_order"),
    path("update-order/<int:pk>/", views.update_order, name="update_order"),
    path("delete-order/<int:pk>/", views.delete_order, name="delete_order"),
]