from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from accounts.models import CustomUser
from accounts.forms import CustomUserForm, CustomAuthenticationForm, CustomPasswordChangeForm, CustomUpdateUserForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from accounts.decorators import superuser_required
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
import json
from products.forms import CategoryForm, ColorForm, ProductForm, SizeForm, StockForm
from django.db.models import Count
from products.models import Category, Code, Color, Product, Size, Stock
from django.core import serializers


# Create your views here.

# Login page
def loginSuperUser(request):
    page = "login"
    form = CustomAuthenticationForm()

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.user_type == 'admin':
                login(request, form.get_user())
                return redirect('superuser-dashboard')
            else:
                messages.error(request, _(
                    "Please enter a correct email and password. Note that both "
                    "fields may be case-sensitive."
                ))
        else:
            print(form.errors)

    context = {'page': page, 'form': form}
    return render(request, 'superuser_login_register.html', context)

# Register page
def registerSuperUser(request):
    page = 'register'
    form = CustomUserForm()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'admin'
            user.save()
            login(request, user)
            return redirect('superuser-dashboard')
        else:
            messages.error(request, form.errors)

    context = {'page': page, 'form': form}
    return render(request, 'superuser_login_register.html', context)

# Logout page
def logoutSuperUser(request):
    page = 'login'
    logout(request)
    
    context = {'page': page}
    return redirect('superuser-login')

# Superuser home page
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def dashboard(request):
    page = 'dashboard'
    
    context = {'page': page}
    return render(request, 'superuser_site/dashboard.html', context)

# Sizes Page
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def sizes(request):
    page = "sizes"
    sizes = Size.objects.all()

    context = {'page': page, 'sizes': sizes}
    return render(request, 'superuser_site/sizes.html', context)

# Add size
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def addSize(request):
    form = SizeForm()
    
    if request.method == 'POST':
        form = SizeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Size Added Successfully!')
            return redirect('sizes')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'superuser_site/add_edit_size.html', context)

# Edit size
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def editSize(request, pk):
    size = Size.objects.get(id=pk)
    form = SizeForm(instance=size)

    if request.method == 'POST':
        form = SizeForm(request.POST, instance=size)
        if form.is_valid():
            form.save()
            messages.success(request, 'Size Updated Successfully!')
            return redirect('sizes')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'superuser_site/add_edit_size.html', context)

# Delete size
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def deleteSize(request, pk):
    size = Size.objects.get(id=pk)

    try:
        if request.method == 'POST':
            size.delete()
            back_to_url = reverse('sizes')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'superuser_site/sizes.html')

# Update activation for size
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def updateSizeActivation(request, pk):
    size = Size.objects.get(id=pk)

    try:
            data = json.loads(request.body)
            data_value = data.get('dataValue', '')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Error', 'error': 'Invalid JSON payload'}, status=400)

    
    try:
        if request.method == 'POST':
            if data_value == '1':
                print(data_value)
                size.active = False
            elif data_value == '0':
                print(data_value)
                size.active = True
            size.save()
            back_to_url = reverse('sizes')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'superuser_site/sizes.html')

# Color page
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def colors(request):
    page = "colors"
    colors = Color.objects.all()

    context = {'page': page, 'colors': colors}
    return render(request, 'superuser_site/colors.html', context)

# Add color
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def addColor(request):
    form = ColorForm()

    if request.method == 'POST':
        form = ColorForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Color Added Successfully!')
            return redirect('colors')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'superuser_site/add_edit_color.html', context)

# Edit color
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def editColor(request, pk):
    color = Color.objects.get(id=pk)
    form = ColorForm(instance=color)

    if request.method == 'POST':
        form = SizeForm(request.POST, instance=color)
        if form.is_valid():
            form.save()
            messages.success(request, 'Color Updated Successfully!')
            return redirect('colors')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'superuser_site/add_edit_color.html', context)

# Delete color
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def deleteColor(request, pk):
    color = Color.objects.get(id=pk)

    try:
        if request.method == 'POST':
            color.delete()
            back_to_url = reverse('colors')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'superuser_site/colors.html')

# Update activation for color
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def updateColorActivation(request, pk):
    color = Color.objects.get(id=pk)

    try:
            data = json.loads(request.body)
            data_value = data.get('dataValue', '')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Error', 'error': 'Invalid JSON payload'}, status=400)

    
    try:
        if request.method == 'POST':
            if data_value == '1':
                print(data_value)
                color.active = False
            elif data_value == '0':
                print(data_value)
                color.active = True
            color.save()
            back_to_url = reverse('colors')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'superuser_site/colors.html')

# Categories page
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def categories(request):
    page = "categories"
    categories = Category.objects.all()

    context = {'categories': categories, 'page': page}
    return render(request, 'superuser_site/categories.html', context)

# Add category
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def addCategory(request):
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category Added Successfully!')
            return redirect('categories')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'superuser_site/add_edit_category.html', context)

# Edit Category
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def editCategory(request, pk):
    category = Category.objects.get(id=pk)
    form = CategoryForm(instance=category)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Updated Successfully!')
            return redirect('categories')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'superuser_site/add_edit_category.html', context)

# Delete Category
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def deleteCategory(request, pk):
    category = Category.objects.get(id=pk)

    try:
        if request.method == 'POST':
            category.delete()
            back_to_url = reverse('categories')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'superuser_site/categories.html')
    
# Update activation for category
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def updateCategoryActivation(request, pk):
    category = Category.objects.get(id=pk)

    try:
            data = json.loads(request.body)
            data_value = data.get('dataValue', '')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Error', 'error': 'Invalid JSON payload'}, status=400)

    
    try:
        if request.method == 'POST':
            if data_value == '1':
                print(data_value)
                category.active = False
            elif data_value == '0':
                print(data_value)
                category.active = True
            category.save()
            back_to_url = reverse('categories')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'superuser_site/cotegories.html')

# All products Page
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def allProducts(request):
    page = "allProducts"
    stocks = Stock.objects.all()

    codes = Code.objects.all()

    total_quantities = {}
    prices = {}
    all_active = {}

    # Calculate data by the code of the product
    for code in codes:
        # Calculate total quantity for each product by its code value
        total_quantity = Stock.calculate_total_quantity(code_value=code)
        total_quantities[code] = total_quantity

        # Calculate min and max price for each product by its code value
        min_price, max_price = Stock.get_price_range(code_value=code)
        prices[code] = {'min_price': min_price, 'max_price': max_price}

        # Check if all is active for each product by its code value
        is_active = Stock.check_all_active(code_value=code)
        all_active[code] = is_active


    

    # Filtering the products objects by the code value with no repeat
    unique_values = set()
    filtered_stocks = []
    for obj in stocks:

        if obj.code not in unique_values:
            filtered_stocks.append(obj)
            unique_values.add(obj.code)

    paginator = Paginator(filtered_stocks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page': page, 'filtered_stocks': filtered_stocks, 'stocks': stocks, 'total_quantities': total_quantities, 'prices': prices, 'all_active': all_active, 'page_obj': page_obj}
    return render(request, 'superuser_site/all_products.html', context)

# Edit all products
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def editAllProduct(request, pk):
    page = 'allProducts'
    product = Product.objects.get(id=pk)
    stock = Stock.objects.get(product=product)
    seller = CustomUser.objects.get(product=product)
    form = ProductForm(instance=product)
    stockForm = StockForm(instance=stock)
    sizes = Size.objects.all()
    colors = Color.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        stockForm = StockForm(request.POST, instance=stock)
        if form.is_valid():
            product = form.save(commit=False)
            product.SKU = str(product.id) + '-' + str(seller.id)
            product.seller = seller
            product.save()

            stock = stockForm.save(commit=False)
            stock.product = product
            stock.size = Size.objects.get(id=request.POST.get('size'))
            stock.color = Color.objects.get(id=request.POST.get('color'))
            stock.save()
            messages.success(request, 'Product Updated Successfully!')

            return redirect('all-products')
        else:
            print(form.errors)
    
    context = {'form': form, 'seller': seller, 'page': page, 'stockForm': stockForm, 'sizes': sizes, 'colors': colors}
    return render(request, 'superuser_site/add_edit_seller_product.html', context)

# Delete all products that have the same code
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def deleteAllProductsCode(request, pk):
    code = get_object_or_404(Stock, product_id = pk).code
    stocks = Stock.objects.filter(code=code)

    try:
        if request.method == 'POST':
            for stock in stocks:
                print("Hii!!")
                product = Product.objects.get(id=stock.product.id)
                print(str(product.name))
                product.delete()
            print(str(code.name))
            code.delete()

            back_to_url = reverse('all-products')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return  render(request, 'superuser_site/all_products.html')

# Delete all products
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def deleteAllProduct(request, pk):
    product = Product.objects.get(id=pk)
    try:
        if request.method == 'POST':
            product.delete()
            back_to_url = reverse('all-products')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return render(request, 'superuser_site/all_products.html')

# Update activation for all products that have the same code
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def updateAllActivationProductsCode(request, pk):
    code = get_object_or_404(Stock, product_id = pk).code
    stocks = Stock.objects.filter(code=code)

    try:
            data = json.loads(request.body)
            data_value = data.get('dataValue', '')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Error', 'error': 'Invalid JSON payload'}, status=400)

    
    try:
        if request.method == 'POST':
            if data_value == '1':
                print(data_value)
                for stock in stocks:
                    stock.product.active = False
                    stock.product.save()
                    print("active: " + str(stock.product.active))

            elif data_value == '0':
                print(data_value)
                for stock in stocks:
                    stock.product.active = True
                    stock.product.save()

            back_to_url = reverse('all-products')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


    return  render(request, 'superuser_site/all_products.html')

# Update activation for all products
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def updateAllActivationProduct(request, pk):
    product = Product.objects.get(id=pk)

    try:
            data = json.loads(request.body)
            data_value = data.get('dataValue', '')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Error', 'error': 'Invalid JSON payload'}, status=400)

    
    try:
        if request.method == 'POST':
            if data_value == '1':
                print(data_value)
                product.active = False
            elif data_value == '0':
                print(data_value)
                product.active = True
            product.save()
            back_to_url = reverse('all-products')
            print(back_to_url)
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'superuser_site/all_products.html')

# Sellers page
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def sellers(request):
    page = "sellers"
    sellers = CustomUser.objects.filter(user_type='seller').annotate(num_products=Count('product'))
    
    context = {'sellers': sellers, 'page': page}
    return render(request, 'superuser_site/sellers.html', context)

# Seller delete page
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def deleteSeller(request, pk):
    seller = CustomUser.objects.get(id=pk)

    try:
        if request.method == 'POST':
            seller.delete()
            back_to_url = reverse('sellers')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'superuser_site/sellers.html')

# Update activation for seller
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def updateActivationSeller(request, pk):
    seller = CustomUser.objects.get(id=pk)

    try:
            data = json.loads(request.body)
            data_value = data.get('dataValue', '')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Error', 'error': 'Invalid JSON payload'}, status=400)
    
    try:
        if request.method == 'POST':
            if data_value == '1':
                print(data_value)
                seller.is_active = False
            elif data_value == '0':
                print(data_value)
                seller.is_active = True
            seller.save()
            back_to_url = reverse('sellers')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'superuser_site/sellers.html')
    

# Seller's Products page
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def sellerProducts(request, pk):
    seller = CustomUser.objects.get(id=pk)
    page = "products"
    products = Product.objects.filter(seller=seller)
    stocks = Stock.objects.filter(product__seller=seller)

    codes = Code.objects.all()

    total_quantities = {}
    prices = {}
    all_active = {}

    # Calculate data by the code of the product
    for code in codes:
        # Calculate total quantity for each product by its code value
        total_quantity = Stock.calculate_total_quantity(code_value=code)
        total_quantities[code] = total_quantity

        # Calculate min and max price for each product by its code value
        min_price, max_price = Stock.get_price_range(code_value=code)
        prices[code] = {'min_price': min_price, 'max_price': max_price}

        # Check if all is active for each product by its code value
        is_active = Stock.check_all_active(code_value=code)
        all_active[code] = is_active


    

    # Filtering the products objects by the code value with no repeat
    unique_values = set()
    filtered_stocks = []
    for obj in stocks:

        if obj.code not in unique_values:
            filtered_stocks.append(obj)
            unique_values.add(obj.code)

    paginator = Paginator(filtered_stocks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products': products, 'page': page, 'seller': seller, 'filtered_stocks': filtered_stocks, 'stocks': stocks, 'total_quantities': total_quantities, 'prices': prices, 'all_active': all_active, 'page_obj': page_obj}
    return render(request, 'superuser_site/all_products.html', context)


# Edit seller's product
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def editSellerProduct(request, pk):
    page = 'allProducts'
    product = Product.objects.get(id=pk)
    stock = Stock.objects.get(product=product)
    seller = CustomUser.objects.get(product=product)
    form = ProductForm(instance=product)
    stockForm = StockForm(instance=stock)
    sizes = Size.objects.all()
    colors = Color.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        stockForm = StockForm(request.POST, instance=stock)
        if form.is_valid():
            product = form.save(commit=False)
            product.SKU = str(product.id) + '-' + str(seller.id)
            product.seller = seller
            product.save()

            stock = stockForm.save(commit=False)
            stock.product = product
            stock.size = Size.objects.get(id=request.POST.get('size'))
            stock.color = Color.objects.get(id=request.POST.get('color'))
            stock.save()
            messages.success(request, 'Product Updated Successfully!')

            return redirect('seller-products', pk=seller.id)
        else:
            print(form.errors)
    
    context = {'form': form, 'seller': seller, 'page': page, 'stockForm': stockForm, 'sizes': sizes, 'colors': colors}
    return render(request, 'superuser_site/add_edit_seller_product.html', context)

# Delete seller products that have the same code
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def deleteSellerProductCode(request, pk):
    code = get_object_or_404(Stock, product_id = pk).code
    stocks = Stock.objects.filter(code=code)
    seller = CustomUser.objects.get(product=stocks[0].product)
    try:
        if request.method == 'POST':
            for stock in stocks:
                print("Hii!!")
                product = Product.objects.get(id=stock.product.id)
                print(str(product.name))
                product.delete()
            print(str(code.name))
            code.delete()

            back_to_url = reverse('seller-products', args=(str(seller.id)))
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return  render(request, 'superuser_site/seller_products.html')

# Delete seller product
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def deleteSellerProduct(request, pk):
    product = Product.objects.get(id=pk)
    seller = CustomUser.objects.get(product=product)
    try:
        if request.method == 'POST':
            product.delete()
            back_to_url = reverse('seller-products', args=(str(seller.id)))
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return render(request, 'superuser_site/seller_products.html')

# Update activation for products that have the same code
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def updateSellerActivationProductCode(request, pk):
    code = get_object_or_404(Stock, product_id = pk).code
    stocks = Stock.objects.filter(code=code)

    try:
            data = json.loads(request.body)
            data_value = data.get('dataValue', '')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Error', 'error': 'Invalid JSON payload'}, status=400)

    
    try:
        if request.method == 'POST':
            if data_value == '1':
                print(data_value)
                for stock in stocks:
                    stock.product.active = False
                    stock.product.save()
                    print("active: " + str(stock.product.active))

            elif data_value == '0':
                print(data_value)
                for stock in stocks:
                    stock.product.active = True
                    stock.product.save()

            back_to_url = reverse('seller-products', args=(str(stocks[0].product.seller.id)))
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


    return  render(request, 'superuser_site/all_products.html')

# Update activation for product
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def updateSellerActivationProduct(request, pk):
    product = Product.objects.get(id=pk)

    try:
            data = json.loads(request.body)
            data_value = data.get('dataValue', '')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Error', 'error': 'Invalid JSON payload'}, status=400)

    
    try:
        if request.method == 'POST':
            if data_value == '1':
                print(data_value)
                product.active = False
            elif data_value == '0':
                print(data_value)
                product.active = True
            product.save()
            back_to_url = reverse('seller-products', args=(str(product.seller.id)))
            print(back_to_url)
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'superuser_site/seller_products.html')

# Customers page    
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def customers(request):
    page = "customers"
    customers = CustomUser.objects.filter(user_type='customer')

    context = {'customers': customers, 'page': page}
    return render(request, 'superuser_site/customers.html', context)

# Customer delete page
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def deleteCustomer(request, pk):
    customer = CustomUser.object.get(id=pk)

    try:
        if request.method == 'POST':
            customer.delete()
            back_to_url = reverse('customers')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'superuser_site/customers.html')

# Update activation for customer
@login_required(login_url='superuser-login')
@superuser_required(redirect_url='superuser-login')
def updateActivationCustomer(request, pk):
    customer = CustomUser.objects.get(id=pk)

    try:
            data = json.loads(request.body)
            data_value = data.get('dataValue', '')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Error', 'error': 'Invalid JSON payload'}, status=400)
    
    try:
        if request.method == 'POST':
            if data_value == '1':
                print(data_value)
                customer.is_active = False
            elif data_value == '0':
                print(data_value)
                customer.is_active = True
            customer.save()
            back_to_url = reverse('customers')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})