from django.urls import path
from . import views

urlpatterns = [
    # Login - Register
    path('login/', views.loginAdmin, name="admin-login"),
    path('register/', views.registerAdmin, name="admin-register"),
    path('logout/', views.logoutAdmin, name="admin-logout"),

    # Dashboard
    path('', views.dashboard, name="dashboard"),

    # Account Settings
    path('account-settings/', views.accountSettings, name="account-settings"),

    # Products URLs
    path('products/', views.products, name="products"),
    path('add-product/', views.addProduct, name="add-product"),
    path('add-product-code/<str:pk>/', views.addProductCode, name="add-product-code"),
    path('edit-product/<str:pk>/', views.editProduct, name="edit-product"),
    path('delete-all-products/<str:pk>/', views.deleteAllProducts, name="delete-all-products"),
    path('delete-product/<str:pk>/', views.deleteProduct, name="delete-product"),
    path('update-all-activation/<str:pk>/', views.updateAllActivation, name="update-all-activation"),
    path('update-activation/<str:pk>/', views.updateActivation, name="update-activation"),
    path('update-dicount-product/<str:pk>/<str:discountPk>/', views.updateProductDiscount, name="update-discount-product"),

    # Discounts URLs
    path('discounts/', views.discounts, name="discounts"),
    path('add-discount/', views.addDiscount, name="add-discount"),
    path('edit-discount/<str:pk>/', views.editDiscount, name="edit-discount"),
    path('delete-dicount/<str:pk>/', views.deleteDiscount, name="delete-discount"),
    path('update-activation-discount/<str:pk>/', views.updateActivationDiscount, name="update-activation-discount"),

]