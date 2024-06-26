from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
import datetime
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required 
import json
from django.core.paginator import Paginator
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else: 
        items = []
        order = {'get_cart_items': 0,'get_cart_total':0}
        cartItems = ['order.get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    products = Product.objects.all()[:6]
    context = {'categories':categories,'products': products, 'cartItems':cartItems,'user_not_login': user_not_login,'user_login':user_login}
    return render(request,'app/home.html', context)
def shop(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else: 
        items = []
        order = {'get_cart_items': 0,'get_cart_total':0}
        cartItems = ['order.get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    products = Product.objects.all()

    # Create a paginator instance
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) if page_number else paginator.page(1)
    context = {'categories':categories,'products': page_obj,'cartItems':cartItems,'user_not_login': user_not_login,'user_login':user_login, 'paginator': paginator,}
    return render(request, 'app/shop.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else: 
        items = []
        order = {'get_cart_items': 0,'get_cart_total':0}
        cartItems = ['order.get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    context = {'categories':categories,'items': items, 'order':order, 'cartItems':cartItems,'user_not_login': user_not_login,'user_login':user_login}
    return render(request,'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else: 
        items = []
        order = {'get_cart_items': 0,'get_cart_total':0}
        cartItems = ['order.get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    context = {'categories':categories,'items': items, 'order':order, 'cartItems':cartItems,'user_not_login': user_not_login,'user_login':user_login}
    return render(request,'app/checkout.html', context)

def register(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form,'user_not_login': user_not_login,'user_login':user_login}
    return render(request,'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        return redirect('home')
    else:
        user_not_login = "show"
        user_login = "hidden"
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password = password)
        if username is not None:
            login(request,user)
            return redirect('home')
        else: 
            messages.info(request, 'Non vl')
    context = {'user_not_login': user_not_login,'user_login':user_login}
    return render(request,'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect ('home')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer= customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('added', safe = False)

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else: 
        user_not_login = "show"
        user_login = "hidden"
        items = []
        order = {'get_cart_items': 0,'get_cart_total':0}
        cartItems = ['order.get_cart_items']
    products = Product.objects.all()
    categories = Category.objects.filter(is_sub = False)
    return render(request,'app/search.html', {'categories':categories,"searched": searched, "keys": keys, 'products': products, 'cartItems':cartItems, 'user_not_login': user_not_login,'user_login':user_login})


def category(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')#cái danh mục đang đc người dùng chọn
    products = Product.objects.all()
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context = {'categories':categories,'products': products, 'active_category': active_category,'user_not_login': user_not_login,'user_login':user_login}
    return render(request,'app/category.html', context)

def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else: 
        items = []
        order = {'get_cart_items': 0,'get_cart_total':0}
        cartItems = ['order.get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    context = {'categories':categories,'items': items, 'order':order, 'cartItems':cartItems,'user_not_login': user_not_login,'user_login':user_login}
    return render(request,'app/detail.html', context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        order.transaction_id = transaction_id
        order.complete = True
        order.save()
        return redirect('home')
    else:
        return redirect('login')

def dashboard(request):
    return render(request, 'app/dashboard.html')