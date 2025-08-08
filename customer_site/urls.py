from django.urls import path
from . import views

urlpatterns = [
    # Login URL
    path('login/', views.loginCustomer, name="login"),

    # Register URL
    path('register/', views.registerCustomer, name="register"),

    # Logout URL
    path('logout/', views.logoutCustomer, name="logout"),

    # Home URL
    path('', views.home, name="home"),

    # All products URL
    path('show-all-products/', views.allProducts, name="show-all-products"),

    # All products with category filter URL
    path('show-all-product-categroy/<str:pk>/', views.allCategoryProducts, name="show-all-products-category"),

    # Product's detail URL
    path('product-detail/<str:pk>/', views.productDetail, name="product-detail"),
]