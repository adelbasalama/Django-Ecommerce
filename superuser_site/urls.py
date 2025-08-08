from django.urls import path
from . import views

urlpatterns = [
    # Login - Register
    path('login/', views.loginSuperUser, name="superuser-login"),
    path('register/', views.registerSuperUser, name="superuser-register"),
    path('logout/', views.logoutSuperUser, name="superuser-logout"),

    # Dashboard
    path('', views.dashboard, name="superuser-dashboard"),

    # Sizes URLs
    path('sizes/', views.sizes, name="sizes"),
    path('add-size/', views.addSize, name="add-size"),
    path('edit-size/<str:pk>/', views.editSize, name="edit-size"),
    path('delete-size/<str:pk>/', views.deleteSize, name="delete-size"),
    path('update-activation-size/<str:pk>/', views.updateSizeActivation, name="update-activation-size"),

    # Colors URLs
    path('colors/', views.colors, name="colors"),
    path('add-color/', views.addColor, name="add-color"),
    path('edit-color/<str:pk>/', views.editColor, name="edit-color"),
    path('delete-color/<str:pk>/', views.deleteColor, name="delete-color"),
    path('update-activation-color/<str:pk>/', views.updateColorActivation, name="update-activation-color"),


    # Categories URLs
    path('categories/', views.categories, name="categories"),
    path('add-category/', views.addCategory, name="add-category"),
    path('edit-category/<str:pk>/', views.editCategory, name="edit-category"),
    path('delete-category/<str:pk>/', views.deleteCategory, name="delete-category"),
    path('update-activation-category/<str:pk>/', views.updateCategoryActivation, name="update-activation-category"),

    # All Products URLs
    path('all-products/', views.allProducts, name="all-products"),
    path('edit-all-product/<str:pk>/', views.editAllProduct, name="edit-all-product"),
    path('delete-all-product/<str:pk>/', views.deleteAllProduct, name="delete-all-product"),
    path('delete-all-products-code/<str:pk>/', views.deleteAllProductsCode, name="delete-all-products-code"),
    path('update-all-activation-product/<str:pk>/', views.updateAllActivationProduct, name="update-all-activation-product"),
    path('update-all-activation-products-code/<str:pk>/', views.updateAllActivationProductsCode, name="update-all-activation-products-code"),

    # Sellers URLs
    path('sellers/', views.sellers, name="sellers"),
    path('delete-seller/<str:pk>/', views.deleteSeller, name="delete-seller"),
    path('update-activation-seller/<str:pk>/', views.updateActivationSeller, name="update-activation-seller"),

    # Seller's Products
    path('seller-products/<str:pk>/', views.sellerProducts, name="seller-products"),
    path('edit-seller-product/<str:pk>/', views.editSellerProduct, name="edit-seller-product"),
    path('delete-seller-product/<str:pk>/', views.deleteSellerProduct, name="delete-seller-product"),
    path('delete-seller-product-code/<str:pk>/', views.deleteSellerProductCode, name="delete-seller-product-code"),
    path('update-seller-activation-product/<str:pk>/', views.updateSellerActivationProduct, name="update-seller-activation-product"),
    path('update-seller-activation-product-code/<str:pk>/', views.updateSellerActivationProductCode, name="update-seller-activation-product-code"),

    # Customer URLs
    path('cusotmers/', views.customers, name="customers"),
    path('delete-customer/<str:pk>/', views.deleteSeller, name="delete-customer"),
    path('update-activation-customer/<str:pk>/', views.updateActivationSeller, name="update-activation-customer"),
]