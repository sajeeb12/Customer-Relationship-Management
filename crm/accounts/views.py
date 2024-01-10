from django.shortcuts import render,redirect
from .models import *
from .forms import  *
from .decorators import allowed_users, unauthenticated_user,admin_only
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


# Create your views here.


# Register
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form =CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, f'Account was created for {username}')
            return redirect('login')
    

    context = {'form':form}
    return render(request,'accounts/register.html',context)




# Login
@unauthenticated_user
def loginPage(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect')
            return render(request,'accounts/login.html')
    return render(request,'accounts/login.html')


# Logout
def logoutUser(request):
    logout(request)
    return redirect('login')


# UserPage
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    order_delivered = orders.filter(status = 'Delivered').count()
    order_pending = orders.filter(status = 'Pending').count()
    context = {'orders':orders,'total_orders':total_orders, 'order_delivered':order_delivered, 'order_pending':order_pending}
    return render(request,'accounts/user.html',context)

# Home

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    

    total_customers = customers.count()
    total_orders = orders.count()
    order_delivered = orders.filter(status = 'Delivered').count()
    order_pending = orders.filter(status = 'Pending').count()

    context = {'customers':customers, 'orders':orders,'total_customers':total_customers,'total_orders':total_orders, 'order_delivered':order_delivered, 'order_pending':order_pending}
    return render(request,'accounts/dashboard.html',context=context)


# Product
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    return render(request,'accounts/product.html',{'products':products})

# Customer
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset= orders)
    orders = myFilter.qs

    context = {'customers':customers,'orders':orders, 'order_count':order_count,'myFilter':myFilter}
    
    return render(request,'accounts/customer.html',context)


# Creating Order
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra =10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset = Order.objects.none(),instance=customer)
    # form = OrderForm(initial = {'customer':customer})

    if request.method =='POST':
        formset = OrderFormSet(request.POST, instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    
    context = {'formset':formset}
    return render(request,'accounts/order_form.html',context)


# Update Order
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request,pk):
    order = Order.objects.get(id = pk)
    form = OrderForm(instance=order)

    if request.method =='POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

# Delete Order
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request,pk):
    order = Order.objects.get(id = pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context ={'order':order}
    return render(request,'accounts/delete_order.html',context=context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method =='POST':
        form = CustomerForm(request.POST,request.FILES, instance= customer)
        if form.is_valid():
            form.save()
    

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)