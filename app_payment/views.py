from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app_order.models import Order, Cart
from app_payment.forms import BllingForm
from app_payment.models import BillingAddress
import  requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
@login_required
def checkedout(request):
    saved_address =  BillingAddress.objects.get_or_create(user=request.user)[0]
    print(saved_address)
    form = BllingForm(instance=saved_address)
    print(form)

    if request.method == "POST":
        form = BllingForm(request.POST,instance=saved_address)
        if form.is_valid():
            form.save()
            form = BllingForm(instance=saved_address)
            messages.success(request, 'Remove Successfully')
    ordrs_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = ordrs_qs[0].orderItems.all()
    order_total = ordrs_qs[0].get_totals()
    return render(request,'app_payment/checkout.html',context={'form':form,'order_items':order_items,'order_total':order_total})

@login_required
def testpayment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)[0]
    if not saved_address.is_fully_fill():
        messages.info(request, 'plz complete shipping address')
        return redirect('app_payment:checkedout')

    if not request.user.profile.is_fully_fill():
        messages.info(request, 'plz complete profile')
        return redirect('loginapp:use_profile')
    store_id = "ab6079637bdc626"
    app_key= "ab6079637bdc626@ssl"
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
                            sslc_store_pass=app_key)
    status_url = request.build_absolute_uri(reverse("app_payment:complete"))
    mypayment.set_urls(success_url=status_url, fail_url=status_url,
                       cancel_url=status_url, ipn_url=status_url)
    ordrs_qs = Order.objects.filter(user=request.user, ordered=False)[0]
    order_items = ordrs_qs.orderItems.all()
    item_count = ordrs_qs.orderItems.count()
    order_total = ordrs_qs.get_totals()
    current_user = request.user
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed',
                                      product_name=order_items, num_of_item=item_count, shipping_method='Cuirer',
                                      product_profile='None')

    mypayment.set_customer_info(name=current_user.profile.fullname, email=current_user.email, address1=current_user.profile.address,
                               address2=current_user.profile.address, city=current_user.profile.city, postcode=current_user.profile.postcode, country=current_user.profile.country,
                               phone=current_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=current_user.profile.fullname, address=saved_address.address, city=saved_address.city, postcode=saved_address.zipcode,
                                country=saved_address.contry)
    response_data = mypayment.init_payment()
    print(response_data)
    return redirect(response_data['GatewayPageURL'])





@csrf_exempt
def complete(request):
    if request.method =="POST" or request.method =="post":
        payment_data = request.POST
        trans_id= payment_data['tran_id']
        val_id= payment_data['val_id']
        bank_tran_id= payment_data['bank_tran_id']
        status= payment_data['status']

        if status == "VALID":
            messages.success(request,"your payment successfully")
            return HttpResponseRedirect(reverse("app_payment:purchase",kwargs={'val_id':val_id,'trans_id':trans_id}))
        elif status == "FAILED":
            messages.success(request, "your payment failed")

    return render(request,'app_payment/complete.html',context={})

@csrf_exempt
def purchase(request,val_id,trans_id):
    qs = Order.objects.filter(user=request.user,ordered=False)[0]

    ordrId = trans_id
    qs.ordered= True
    qs.paymentId = ordrId
    qs.orderId = val_id
    qs.save()
    cart_val = Cart.objects.filter(user=request.user,purchased=False)
    for item in cart_val:
        item.purchased = True
        item.save()



    return HttpResponseRedirect(reverse("app_shop:index"))
