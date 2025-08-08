from django.db import models
from django.db.models import Min, Max
import os

from accounts.models import CustomUser

# Create your models here.

# Discount Model
class Discount(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=250, null=True)
    discount_percent = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# Category Model
class Category(models.Model):
    name = models.CharField(max_length=200)
    category_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.CharField(max_length=250, null=True, blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_full_path()
    
    def get_full_path(self):
        path = [self.name]
        current_category = self
        while current_category.category_parent:
            current_category = current_category.category_parent
            path.insert(0, current_category.name)
        return ' / '.join(path)
    
    def get_descendants_ids(self):
        """
        Returns a set of IDs of all descendants of this category, including itself.
        """
        descendants_ids = set()
        self._collect_descendants_ids(descendants_ids)
        return descendants_ids

    def _collect_descendants_ids(self, descendants_ids):
        """
        Recursively collects the IDs of all descendants of this category, including itself.
        """
        descendants_ids.add(self.pk)
        for child in Category.objects.filter(category_parent=self):
            child._collect_descendants_ids(descendants_ids)


# Product Size Model
class Size(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# Product Color Model
class Color(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

# Product Code Model
class Code(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    SKU = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=200)
    cart_desc = models.CharField(max_length=250, null=True)
    short_desc = models.CharField(max_length=1000, null=True)
    long_desc = models.TextField(blank=True, null=True)
    thumb = models.ImageField(upload_to='images/', null=True, blank=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    # product_image =
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.FloatField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        # Remove the associated image file from the file system
        if self.thumb:
            if os.path.isfile(self.thumb.path):
                os.remove(self.thumb.path)
        
        super(Product, self).delete(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount is not None:
            discount_factor = 1 - (self.discount.discount_percent / 100)
        else:
            discount_factor = 1
        return self.price * discount_factor 

    def __str__(self):
        return self.name
    

# Stock Model
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @classmethod
    def calculate_total_quantity(cls, code_value):
        total_quantity = 0
        stocks = cls.objects.filter(code=code_value)
        for stock_item in stocks:
            total_quantity += stock_item.quantity
        return total_quantity
    
    @classmethod
    def get_price_range(cls, code_value):
        products = Product.objects.filter(stock__code=code_value)
        if products.exists():
            min_price = min(product.discounted_price for product in products)
            max_price = max(product.discounted_price for product in products)
        else:
            min_price = 0
            max_price = 0
        return min_price, max_price
    
    @classmethod
    def check_all_active(cls, code_value):
        stocks_1 = cls.objects.filter(code=code_value)
        for stock in stocks_1:
            if stock.product.active == False:
                return False
            
        return True
            
    
    def __int__(self):
        return self.quantity
    





