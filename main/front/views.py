from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main import models

def index(request):
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    reviews = models.Review.objects.all()

    mark = 0
    for i in reviews:
        mark += i.mark
    
    mark = int(mark/len(reviews)) if reviews else 0
    context = {
        'categories':categories,
        'products':products,
        'rating':range(1,6),
        'mark':mark,
        }
    return render(request, 'front/index.html',context)


def add_cart(request, code):
    product = models.Product.objects.get(code=code)
    cart , _ = models.Cart.objects.get_or_create(user=request.user, is_active=True)
    cart_product , _ = models.CartProduct.objects.get_or_create(cart=cart, product=product, count=1)
    cart_product.save()
    return redirect('front:index')

def remove_cart(request, code):
    if request.method == 'GET':
        cart = get_object_or_404(models.Cart, user=request.user, is_active=True)
        product = get_object_or_404(models.Product, code=code)

        cart_products = models.CartProduct.objects.filter(cart=cart, product=product)

        if cart_products.exists():
            cart_products.delete() 

    return redirect('front:active_cart')


def update_quantity(request, code):
    if request.method == 'POST':
        product = models.Product.objects.get(code=code)
        quantity = int(request.POST.get('quantity', 0))
        action = request.POST.get('action')
        cart, _ = models.Cart.objects.get_or_create(user=request.user, is_active=True)
        
        cart_product = models.CartProduct.objects.filter(cart=cart, product=product).first()
        
        if not cart_product:
            cart_product = models.CartProduct.objects.create(cart=cart, product=product, count=0)

        if action == 'increase':
            cart_product.count += 1
        elif action == 'decrease':
            if cart_product.count > 1:
                cart_product.count -= 1

        cart_product.save()

    return redirect('front:active_cart')



def product_detail(request,code):
    product = models.Product.objects.get(code=code)
    reviews = models.Review.objects.filter(product=product)
    images = models.ProductImg.objects.filter(product=product)
    mark = 0

    for i in reviews:
        mark += i.mark

    mark = int(mark/len(reviews)) if reviews else 0
    context = {
        'product':product,
        'mark':mark,
        'rating':range(1,6),
        'images':images,
        'reviews':reviews,
    }
    return render(request, 'front/product/detail.html',context)

def product_list(request,id):
    queryset = models.Product.objects.filter(category_id=id)
    categories = models.Category.objects.all()
    context = {
        'queryset':queryset,
        'categories':categories,
        }
    return render(request, 'front/category/product_list.html',context)


@login_required(login_url='auth:login')
def carts(request):
    queryset = models.Cart.objects.filter(user=request.user, is_active=False)
    context = {'queryset':queryset}
    return render(request, 'front/carts/list.html', context)


@login_required(login_url='auth:login')
def active_cart(request):
    queryset , _ = models.Cart.objects.get_or_create(user=request.user, is_active=True)
    return redirect('front:cart_detail', queryset.code)


@login_required(login_url='auth:login')
def cart_detail(request, code):
    cart = models.Cart.objects.get(code=code)
    queryset = models.CartProduct.objects.filter(cart=cart)
    context = {
        'cart': cart,
        'queryset':queryset
        }
    return render(request, 'front/carts/detail.html', context)
