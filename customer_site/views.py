from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect
from accounts.forms import CustomAuthenticationForm, CustomUserForm
from products.models import Product, Category
from django.contrib.auth import login, logout, update_session_auth_hash

from django.utils.translation import gettext_lazy as _

# Create your views here.

# Login page
def loginCustomer(request):
    page = "login"
    form = CustomAuthenticationForm()

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.user_type == 'customer':
                login(request, form.get_user())
                return redirect('home')
            else:
                messages.error(request, _(
                    "Please enter a correct email and password. Note that both "
                    "fields may be case-sensitive."
                ))
        else:
            print(form.errors)

    context = {'form': form, 'page': page}
    return render(request, 'customer_login_register.html', context)

# Register page
def registerCustomer(request):
    page = "register"
    form = CustomUserForm()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'customer'
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, form.errors)

    context = {'page': page, 'form': form}
    return render(request, 'customer_login_register.html', context)

# Logout page
def logoutCustomer(request):
    page = 'login'
    logout(request)
    
    context = {'page': page}
    return redirect('login')

# Home page
def home(request):
    categories = Category.objects.filter(category_parent__isnull=True)

    context = {'categories': categories}
    return render(request, 'customer_site/home.html', context)

# All products page
def allProducts(request):
    page = "All Products"
    products = Product.objects.filter(active=True)
    paginator = Paginator(products, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products': products, 'page_obj': page_obj, 'page': page}
    return render(request, 'customer_site/show_all_products.html', context)

# All products with category filter
def allCategoryProducts(request, pk):
    categories = Category.objects.filter(category_parent__isnull=True)
    category = Category.objects.get(id=pk)
    page = category
    products = Product.objects.filter(category=category)
    paginator = Paginator(products, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'categories': categories, 'products': products, 'page_obj': page_obj, 'page': page}
    return render(request, 'customer_site/show_all_products.html', context)

# Product's detail page
def productDetail(request, pk):
    page = "Product Details"
    product = Product.objects.get(id=pk)

    context = {'page': page, 'product': product}
    return render (request, 'customer_site/product_detail.html', context)