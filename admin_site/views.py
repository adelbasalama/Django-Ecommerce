from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.utils.html import escape
from django.contrib import messages
from accounts.models import CustomUser
from accounts.forms import CustomUserForm, CustomAuthenticationForm, CustomPasswordChangeForm, CustomUpdateUserForm
from accounts.decorators import seller_required
from products.models import Code, Color, Product, Discount, Size, Stock
from products.forms import ProductForm, DiscountForm, StockForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json
from django.contrib.auth import login, logout, update_session_auth_hash
from django.utils.translation import gettext_lazy as _


# Login page
def loginAdmin(request):
    page = "login"
    form = CustomAuthenticationForm()

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.user_type == 'seller':
                login(request, form.get_user())
                return redirect('dashboard')
            else:
                messages.error(request, _(
                    "Please enter a correct email and password. Note that both "
                    "fields may be case-sensitive."
                ))
        else:
            print(form.errors)

    context = {'page': page, 'form': form}
    return render(request, 'login_register.html', context)

# Register page
def registerAdmin(request):
    page = 'register'
    form = CustomUserForm()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'seller'
            user.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, form.errors)

    context = {'page': page, 'form': form}
    return render(request, 'login_register.html', context)

# Logout page
def logoutAdmin(request):
    page = 'login'
    logout(request)
    
    context = {'page': page}
    return redirect('admin-login')

# admin home page
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def dashboard(request):
    page = "dashboard"
    context = {'page': page}
    return render(request, 'admin_site/dashboard.html', context)

# admin account settings
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def accountSettings(request):
    user = request.user
    form = CustomUpdateUserForm(instance=request.user)
    changePasswordForm = CustomPasswordChangeForm(request.user)

    if request.method == 'POST':
        changePasswordForm = CustomPasswordChangeForm(request.user, request.POST)
        form = CustomUpdateUserForm(request.POST, request.FILES, instance=user)
        if changePasswordForm.is_valid():
            messages.success(request, 'Password Updated Successfully!')
            changePasswordForm.save()
            update_session_auth_hash(request, request.user)
            return redirect('account-settings')
        elif form.is_valid():
            form.save()
            messages.success(request, 'Account Updated Successfully!')
            return redirect('account-settings')
        else:
            print(form.errors)
            messages.error(request, changePasswordForm.errors)

    context = {'user': user, 'form': form, 'changePasswordForm': changePasswordForm}
    return render(request, 'admin_site/account_settings.html', context)


# admin products page
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def products(request):
    user = request.user
    page = "products"
    products = Product.objects.filter(seller=user)
    stocks = Stock.objects.filter(product__seller=user)

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

    discounts = Discount.objects.filter(active=True)
    context = {'products': products, 'discounts': discounts, 'page': page, 'user': user, 'filtered_stocks': filtered_stocks, 'stocks': stocks, 'total_quantities': total_quantities, 'prices': prices, 'all_active': all_active, 'page_obj': page_obj}
    return render(request, 'admin_site/products.html', context)

# Add products
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def addProduct(request):
    form = ProductForm()
    stockForm = StockForm()
    sizes = Size.objects.all()
    colors = Color.objects.all()
    codes = Code.objects.all()
    codeId = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        stockForm = StockForm(request.POST)
        if form.is_valid() and stockForm.is_valid():
            if request.POST.get('new-code') != "":
                codeId = Code.objects.create(name=request.POST.get('new-code'))

            
            product = form.save()
            product.SKU = str(product.id) + '-'+ str(request.user.id)
            product.seller = request.user
            product.save()

            stock = stockForm.save(commit=False)
            stock.product = product
            stock.size = Size.objects.get(id=request.POST.get('size'))
            stock.color = Color.objects.get(id=request.POST.get('color'))
            stock.code = codeId if codeId is not None else Code.objects.get(id=request.POST.get('code'))
            stock.save()    
            print('done!')
            messages.success(request, 'Product Added Successfully!')
            return redirect('products')
        else:
            print(form.errors)
    
    context = {'form': form, 'stockForm': stockForm, 'sizes': sizes, 'colors': colors, 'codes': codes}
    return render(request, 'admin_site/add_edit_product.html', context)

# Add different size of the same product
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def addProductCode(request, pk):
    product = Product.objects.get(id=pk)
    stock = Stock.objects.get(product=product)
    form = ProductForm(instance=product)
    stockForm = StockForm()
    currentCode = Code.objects.get(stock=stock)
    currentImage = product.thumb
    sizes = Size.objects.all()
    colors = Color.objects.all()
    codes = Code.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        stockForm = StockForm(request.POST)
        if form.is_valid() and stockForm.is_valid():
            product = form.save()
            product.SKU = str(product.id) + '-'+ str(request.user.id)
            product.seller = request.user
            product.thumb = currentImage
            product.save()

            stock = stockForm.save(commit=False)
            stock.product = product
            stock.size = Size.objects.get(id=request.POST.get('size'))
            stock.color = Color.objects.get(id=request.POST.get('color'))
            stock.code = currentCode
            stock.save()    
            print('done!')
            messages.success(request, 'Product Added Successfully!')
            return redirect('products')
        else:
            print(form.errors)
    
    context = {'form': form, 'stockForm': stockForm, 'sizes': sizes, 'colors': colors, 'codes': codes, 'currentCode': currentCode}
    return render(request, 'admin_site/add_edit_product.html', context)

# Edit product
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def editProduct(request, pk):
    product = Product.objects.get(id=pk)
    stock = Stock.objects.get(product=product)
    form = ProductForm(instance=product)
    stockForm = StockForm(instance=stock)
    currentCode = Code.objects.get(stock=stock)
    sizes = Size.objects.all()
    colors = Color.objects.all()
    codes = Code.objects.all()
    codeId = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        stockForm = StockForm(request.POST, instance=stock)
        if form.is_valid() and stockForm.is_valid():
            if request.POST.get('new-code') != "":
                codeId = Code.objects.create(name=request.POST.get('new-code'))

            
            product = form.save()
            product.SKU = str(product.id) + '-'+ str(request.user.id)
            product.seller = request.user
            product.save()

            stock = stockForm.save(commit=False)
            stock.product = product
            stock.size = Size.objects.get(id=request.POST.get('size'))
            stock.color = Color.objects.get(id=request.POST.get('color'))
            stock.code = codeId if codeId is not None else Code.objects.get(id=request.POST.get('code'))
            stock.save()    
            print('done!')
            messages.success(request, 'Product Added Successfully!')
            return redirect('products')
        else:
            print(form.errors)
    
    context = {'form': form, 'stockForm': stockForm, 'sizes': sizes, 'colors': colors, 'codes': codes, 'currentCode': currentCode}
    return render(request, 'admin_site/add_edit_product.html', context)


# Delete all products that has the same code
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def deleteAllProducts(request, pk):
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

            back_to_url = reverse('products')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return  render(request, 'admin_site/products.html')

# Delete product
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)

    try:
        if request.method == 'POST':
            product.delete()
            back_to_url = reverse('products')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return  render(request, 'admin_site/products.html')

# Update all activation for products that have the same code
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def updateAllActivation(request, pk):
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

            back_to_url = reverse('products')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


    return  render(request, 'admin_site/products.html')


# Update activation for product
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def updateActivation(request, pk):
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
            back_to_url = reverse('products')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


    return  render(request, 'admin_site/products.html')

# Update the discount for a product
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def updateProductDiscount(request, pk, discountPk):
    product = Product.objects.get(id=pk)
    discount = Discount.objects.get(id=discountPk)

    try:
        data = json.loads(request.body)
        data_value = data.get('dataValue','')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Error', 'error': 'Invalid JSON payload'}, status=400)
    
    try:
        if request.method == 'POST':
            if data_value == '1':
                product.discount = None
            elif data_value == '0':
                product.discount = discount
            product.save()
            back_to_url = reverse('products')
            return JsonResponse({'success': True, 'message': 'Discount added successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        print(str(e))
        return JsonResponse({'success': False, 'message': str(e)})


    return render(request, 'admin_site/products.html')


# admin discounts page
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def discounts(request):
    page = "discounts"
    discounts = Discount.objects.all()
    context = {'discounts': discounts, 'page': page}
    return render(request, 'admin_site/discounts.html', context)

# Add Discount
def addDiscount(request):
    form = DiscountForm()
    if request.method == 'POST':
        form = DiscountForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Discount Added Successfully!')
            return redirect('discounts')
        else:
            print(form.errors)
    

    context = {'form': form}
    return render(request, 'admin_site/add_edit_discount.html', context)

# Edit Discount
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def editDiscount(request, pk):
    discount = Discount.objects.get(id=pk)
    form = DiscountForm(instance=discount)
    print(form)

    if request.method == 'POST':
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            discount = form.save(commit=False)
            if not discount.active:
                discount.product_set.update(discount=None)
            discount.save()
            messages.success(request, 'Discount Updated Successfully!')
            return redirect('discounts')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'admin_site/add_edit_discount.html', context)


# Delete Discount
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def deleteDiscount(request, pk):
    discount = Discount.objects.get(id=pk)

    try:
        if request.method == 'POST':
            discount.delete()
            back_to_url = reverse('discounts')
            return JsonResponse({'success': True, 'message': 'Data deleted successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    return render(request, 'admin_site/discounts.html')

# Update activation for discount
@login_required(login_url='admin-login')
@seller_required(redirect_url='admin-login')
def updateActivationDiscount(request, pk):
    discount = Discount.objects.get(id=pk)

    try:
            data = json.loads(request.body)
            data_value = data.get('dataValue', '')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Error', 'error': 'Invalid JSON payload'}, status=400)
    
    try:
        if request.method == 'POST':
            if data_value == '1':
                print(data_value)
                discount.active = False
                discount.product_set.update(discount=None)
            elif data_value == '0':
                print(data_value)
                discount.active = True
            discount.save()
            back_to_url = reverse('discounts')
            return JsonResponse({'success': True, 'message': 'Data updated successfully.', 'back_to_url': back_to_url})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


    return render(request, 'admin_site/products.html')
