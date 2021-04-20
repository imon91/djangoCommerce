from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from app_order.models import Cart, Order
from app_shop.models import Product


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    ordrs_qs = Order.objects.filter(user=request.user, ordered=False)
    if ordrs_qs.exists():
        order = ordrs_qs[0]
        if order.orderItems.filter(item=item).exists():
            print(order_item[0].quantity)
            order_item[0].quantity += 1
            order_item[0].save()
            return redirect("app_shop:index")

        else:
            order.orderItems.add(order_item[0])
            return redirect("app_shop:index")

    else:
        order = Order(user=request.user)
        order.save()
        order.orderItems.add(order_item[0])
        return redirect("app_shop:index")

@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    order = orders[0]

    return render(request, 'app_order/cart.html', {'carts': carts, 'order': order})
@login_required
def remove_cart_item(request,pk):
    item = get_object_or_404(Product, pk=pk)
    # order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    ordrs_qs = Order.objects.filter(user=request.user, ordered=False)
    if ordrs_qs.exists():
        order = ordrs_qs[0]
        if order.orderItems.filter(item=item).exists():
            order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)[0]
            order.orderItems.remove(order_item)
            order_item.delete()
            messages.success(request, 'Remove Successfully')
            return redirect('app_order:cart_view')

        else:
            messages.success(request, 'cant change')
            return redirect('app_order:cart_view')

    else:
        messages.info(request, 'this product is not your cart')
        return redirect('app_shop:index')


@login_required
def increase_product(request,pk):
    items = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=items, user=request.user, purchased=False)[0]
    ordrs_qs = Order.objects.filter(user=request.user, ordered=False)
    if ordrs_qs.exists():
        order_item.quantity += 1
        order_item.save()
        return redirect('app_order:cart_view')

    else:
        messages.info(request, 'this product is not your cart')
        return redirect('app_shop:index')

def decrease_product(request,pk):
    items = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=items, user=request.user, purchased=False)[0]
    ordrs_qs = Order.objects.filter(user=request.user, ordered=False)
    if ordrs_qs.exists():
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
            return redirect('app_order:cart_view')
        else:
            messages.info(request, 'You Can not make quantity value is null')
            return redirect('app_order:cart_view')

    else:
        messages.info(request, 'this product is not your cart')
        return redirect('app_shop:index')



