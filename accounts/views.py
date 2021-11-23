from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages, auth

from .models import Order, Customer, Product, Tag
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {

    }
    return render(request , 'accounts/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('login')




def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')


    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)



@login_required(login_url="login")
def home(request):
    orders = Order.objects.all().order_by('-date_created')
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url="login")
def products(request):
    products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)

@login_required(login_url="login")
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs # querysetni qo'shadi orders ni ustidan override qiladi

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter
    }
    return render(request, 'accounts/customers.html', context)


@login_required(login_url="login")
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=2)
    customer = Customer.objects.get(pk=pk)
    formset = OrderFormSet(queryset = Order.objects.none(),instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        # form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("home")

    context = {
        'formset': formset
    } 
    return render(request, 'accounts/order_form.html', context)



@login_required(login_url="login")
def update_order(request, pk):
    order = Order.objects.get(pk=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url="login")
def delete_order(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {
        'item': order
    }
    return render(request, 'accounts/delete.html', context)