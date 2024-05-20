from django.urls import path
from . import views


app_name = 'front'


urlpatterns = [
    path('', views.index, name='index'),
    # Products
    path('product/<str:code>', views.product_detail, name='product_detail'),
    path('category/<str:code>', views.product_list, name='product_list'),
    path('category/', views.product_list, name='all_product_list'),
    # Carts
    path('carts/', views.carts, name='carts'),
    path('cart/<str:code>/', views.cart_detail, name='cart_detail'),
    path('active-cart', views.active_cart, name='active_cart'),
    path('add-cart/<str:code>/', views.add_cart, name='add_cart'),
    path('remove-cart/<str:code>/', views.remove_cart, name='remove_cart'),
    path('update-quantity/<str:code>/', views.update_quantity, name='update_quantity'),
    # Product order and return
    path('product-order/', views.product_order, name='product_order'),
    path('product-return/<str:code>/', views.product_return, name='product_return'),
    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-wishlist/<str:code>/', views.add_wishlist, name='add_wishlist'),
    path('remove-wishlist/<str:code>/', views.remove_wishlist, name='remove_wishlist'),
    # Review
    path('add-review/<str:code>/', views.add_review, name='add_review'),
    # Downloading pdf
    path('download-pdf/<str:code>/', views.download_pdf, name='download_pdf')
]