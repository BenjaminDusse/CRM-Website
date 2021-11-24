from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import Order, Customer, Product, Tag
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
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

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name="customer")
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


@login_required(login_url="login")
@admin_only
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


@allowed_users(allowed_roles=['customer'])
def userPage(request):



    context = {}
    return render(request, 'accounts/user.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs  # querysetni qo'shadi orders ni ustidan override qiladi

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter
    }
    return render(request, 'accounts/customers.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=2)
    customer = Customer.objects.get(pk=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {
        'item': order
    }
    return render(request, 'accounts/delete.html', context)
