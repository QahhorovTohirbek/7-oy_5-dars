from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main import models


from django.shortcuts import redirect

def index(request):
    if not request.user.is_authenticated:
        return redirect('auth:login') 

    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    wishlist = models.WishList.objects.filter(user=request.user)
    reviews = models.Review.objects.all()


    mark = 0
    for i in reviews:
      mark += i.mark
     
    mark = int(mark/len(reviews)) if reviews else 0
    context = {
        'categories':categories,
        'products':products,
        'wishlist':wishlist,
        'rating':range(1,6),
        'mark':mark,
        }

    return render(request, 'front/index.html', context)


@login_required(login_url='auth:login')
def add_cart(request, code):
    product = models.Product.objects.get(code=code)
    cart, _ = models.Cart.objects.get_or_create(user=request.user, is_active=True)
    
    try:
        cart_product = models.CartProduct.objects.get(cart=cart, product=product)
        cart_product.count += 1
        cart_product.save()
    except models.CartProduct.DoesNotExist:
        cart_product = models.CartProduct.objects.create(cart=cart, product=product, count=1)

    return redirect('front:index')


@login_required(login_url='auth:login')
def remove_cart(request, code):
    if request.method == 'GET':
        cart = get_object_or_404(models.Cart, user=request.user, is_active=True)
        product = get_object_or_404(models.Product, code=code)

        cart_products = models.CartProduct.objects.filter(cart=cart, product=product)

        if cart_products.exists():
            cart_products.delete() 

    return redirect('front:active_cart')


@login_required(login_url='auth:login')
def update_quantity(request, code):
    if request.method == 'POST':
        product = models.Product.objects.get(code=code)
        action = request.POST.get('action')
        cart, _ = models.Cart.objects.get_or_create(user=request.user, is_active=True)
        
        cart_product = models.CartProduct.objects.filter(cart=cart, product=product).first()

        if action == 'increase':
            cart_product.count += 1
        elif action == 'decrease':
            if cart_product.count > 1:
                cart_product.count -= 1
            else:
                cart_product.delete()
                return redirect('front:active_cart')

            cart_product.save()

        return redirect('front:active_cart')


@login_required(login_url='auth:login')
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


@login_required(login_url='auth:login')
def product_list(request,code):
    queryset = models.Product.objects.filter(category__code=code)
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


@login_required(login_url='auth:login')
def product_order(request):
    cart = models.Cart.objects.get(user=request.user, is_active=True)

    cart.is_active = False
    cart.save()

    return redirect('front:carts')


@login_required(login_url='auth:login')
def wishlist(request):
    queryset = models.WishList.objects.filter(user=request.user)
    context = {
        'queryset':queryset
    }
    return render(request, 'front/wishlist/list.html', context)



@login_required(login_url='auth:login')
def add_wishlist(request, code):
    product = get_object_or_404(models.Product, code=code)
    wishlist = models.WishList.objects.filter(product=product, user=request.user)
    if models.WishList.objects.filter(product=product, user=request.user).exists():
        wishlist.delete()
    else:
        wishlist = models.WishList.objects.create(product=product, user=request.user)
    return redirect('front:wishlist')

@login_required(login_url='auth:login')
def remove_wishlist(request, code):
    wishlist = get_object_or_404(models.WishList, product__code=code, user=request.user)
    wishlist.delete()
    return redirect('front:wishlist')

