from django import forms
from django.forms import ModelForm
from django.forms.widgets import ClearableFileInput
from .models import Color, Product, Discount, Category, Size, Stock

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Description'}),
            'active': forms.CheckboxInput(attrs={'name': 'my-checkbox'}),
            'category_parent': forms.Select(attrs={'class': 'custom-select'})
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        # Get the instance if it exists
        instance = kwargs.get('instance')
        # Exclude the current category and its descendants from the queryset
        if instance:
            excluded_ids = instance.get_descendants_ids()
            self.fields['category_parent'].queryset = Category.objects.exclude(pk__in=excluded_ids)
        else:
            self.fields['category_parent'].queryset = Category.objects.all()

    def get_excluded_category_ids(self, category):
        """
        Recursively get the IDs of the category and its descendants.
        """
        descendants = category.get_descendants_ids(include_self=True)
        return descendants.values_list('pk', flat=True)

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'SKU': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product SKU'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Color'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'custom-select'}),
            'cart_desc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Cart Description'}),
            'short_desc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Short Description'}),
            'long_desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Product Long Description'}),
            'thumb': forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'exampleInputFile'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px', 'min': '0'}),
            'active': forms.CheckboxInput(attrs={'name': 'my-checkbox'}),

        }

class SizeForm(ModelForm):
    class Meta:
        model = Size
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Discount Description'}),
        }

class ColorForm(ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Discount Description'}),
        }

class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px', 'min': '0'}),
        }


class DiscountForm(ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Discount Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Discount Description'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px', 'min': '0'}),
            'active': forms.CheckboxInput(attrs={'name': 'my-checkbox'}),
        }