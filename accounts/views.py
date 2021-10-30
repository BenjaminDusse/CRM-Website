from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    context = {}
    return render(request, 'accounts/products.html', context)

def customers(request):
    context = {}
    return render(request, 'accounts/customers.html', context)