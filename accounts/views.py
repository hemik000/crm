from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from .models import Customer, Product, Order
from .forms import OrdesForm, UserReg, UserLogin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import urls
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import reverse
# Create your views here.




@login_required()
def home(request):
    # if not request.user.groups.filter(name='admin').exists():
        # HttpResponse.status_code = 403
        # return HttpResponse('You don\'t have authorization to view this page.', status=403)
    if request.user.groups.filter(name='customer').exists():
        return redirect(reverse('customer'))

    custs = Customer.objects.all()
    ords = Order.objects.all()
    total_orders = ords.count()
    total_orders_delivered = ords.filter(status="Delivered").count()
    total_orders_pending = ords.filter(status="Pending").count()

    context = {
        'custs': custs,
        'ords': ords,
        'total_orders': total_orders,
        'total_orders_delivered': total_orders_delivered,
        'total_orders_pending': total_orders_pending
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required()
def products(request):
    pros = Product.objects.all()
    context = {
        'pros': pros
    }
    return render(request, 'accounts/products.html', context)


@login_required()
def customer(request, id=None):
    if id is None and request.user.groups.filter(name='customer').exists():
        id = request.user.customer.id
    elif id and not request.user.groups.filter(name='admin').exists():
        return HttpResponse('You don\'t have authorization to view this page.', status=403)
    elif id is None and request.user.groups.filter(name='admin').exists():
        return redirect(reverse('home'))

    cust = Customer.objects.get(id=id)
    ords = cust.order_set.all()

    context = {
        'cust': cust,
        'ords': ords
    }

    return render(request, 'accounts/customer.html', context)

@login_required()
def update(request, id):
    if request.user.groups.filter(name='customer') and not Order.objects.get(id=id).customer.user.id == request.user.id:
        return HttpResponse('Invalid Order ID')
        
    ord = Order.objects.get(id=id)
    form = OrdesForm(instance=ord)

    if request.method == 'POST':
        form = OrdesForm(request.POST, instance=ord)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form' : form
    }
    
    return render(request, 'accounts/update.html', context )


@login_required()
def create(request):
    # print(request.user)
    if request.method == 'POST':
        form = OrdesForm(request.POST)
        if form.is_valid():
            form.instance.customer = request.user.customer
            form.save()
            return redirect('/')
    else:
        form = OrdesForm()

        # print(request.user.customer)


    context = {
        'form' : form
    }
    return render(request, 'accounts/create.html', context)




class LoginPage(LoginView):
    form_class = UserLogin
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


def logoutPage(request):
    logout(request)
    return redirect('login')


def register(request):
    form = UserReg()
    if request.method == 'POST':
        form = UserReg(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)
