from typing import ValuesView
from bazaar.settings import MESSAGE_TAGS
from ecom.forms import AddressForm
from django.shortcuts import render,get_object_or_404,redirect
from ecom.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.decorators import login_required


import random
import string
from django.contrib import messages


# from django.utils import timezone
from django.utils import timezone

import urllib
import urllib.request
import urllib.parse

def send(r,mobile,msg):
    authkey = "asdfghjkrtyuiasdfghj"
    mobiles = mobile
    message = msg

    sender = "mzdvyud"
    values = {
        'authkey': authkey,
        'mobiles':mobiles,
        'message': message,
        'sender': sender,
        'route':4,


    }
    url = "http://api.msg91.com/api/sendhttp.php"   #API URL
    postdata = urllib.parse.urlencode(values)   #url encoding the data here
    postdata = postdata.encode('utf-8')
    req = urllib.request.Request(url,postdata)
    response = urllib.request.urlopen(req)
    output = response.read() #Get response



def homepages(request):
    data = {"item":Item.objects.all(),"cat":Category.objects.all()}
    return render(request,"public/home.html",data)


def productView(request,slug):
    data = {
        "item":Item.objects.get(slug=slug),
        "cat":Category.objects.all()
        }
    return render(request,"public/product.html",data)

def searchView(request):
    if request.method =="GET":
        search = request.GET.get('search')
        data = {
                "item":Item.objects.filter(title__icontains=search),
                "cat":Category.objects.all()
                }
    return render(request,"public/home.html",data)


def categoryView(request,cat_slug):
    data = {
        "item":Item.objects.filter(category__slug=cat_slug),
        "cat":Category.objects.all()
        }
    return render(request,"public/home.html",data)


@login_required()
def addTocart(req,slug):
    item = get_object_or_404(Item,slug=slug)

    orderItem, created = OrderItem.objects.get_or_create(
        item = item,
        user = req.user,
        ordered = False
    )

    order_qs = Order.objects.filter(user=req.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():

            orderItem.qty += 1
            orderItem.save()
            # todo msg:  this item is updated in your card
            return redirect(orderSummery)
            
        else:

            order.items.add(orderItem)
            # todo : this item is added in your card successfully
            return redirect(orderSummery)
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=req.user,ordered=False,start_date=order_date)
        order.items.add(orderItem)
        order.save()
        # todo msg: this item was added to your card
        redirect(orderSummery)

@login_required()
def remove_from_cart_single(req,slug):
    item = get_object_or_404(Item,slug=slug)

    orderItem, created = OrderItem.objects.get_or_create(
        item = item,
        user = req.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user=req.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = req.user,
                ordered = False
            )[0]

            if order_item.qty > 1:
                order_item.qty -= 1
                order_item.save()
            else:
                                
                order.items.remove(order_item)
                # todo msg: item update successfully
                messages.error(req,"item delete successfully")
            return redirect(orderSummery)
        else:
            messages.error(req,"This item is not availabble in your cart")
            #todo msg: this item is not availabble in your cart
            return redirect(orderSummery)
    else:
        messages.info(req,"you not have in active order")
        #todo msg: you not have in active order
        return redirect(orderSummery)


@login_required()
def orderSummery(req):
    try:
        order = Order.objects.get(user=req.user,ordered=False)
    except ObjectDoesNotExist:
        return redirect("home")
    data = {"order": order}

    return render(req, "public/cart.html",data)

@login_required
def checkout(req):
    form = AddressForm(req.POST or None)
    if req.method == "POST":
        if form.is_valid():
            f = form.save(commit=False)
            f.user = req.user
            f.save()
            return redirect("checkout")



    data = {
        "addressform":form,
        "address":Address.objects.filter(user=req.user)
    }
    return render(req, "public/checkout.html",data)
def get_ref_code(digit):
    return ''.join(random.choices(string.digits,k=digit))

def checkCouponCode(code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        return False
def getCoupon(req,code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        #msg : this coupon doesn't match
        return redirect("cart")



def addCoupon(req):
    if req.method == "POST":
        code = req.POST.get("code")
        if checkCouponCode(code):
            
            order = Order.objects.get(user=req.user,ordered=False)
            coupon = getCoupon(req,code)
            if order.get_total_amount() > coupon.amount:
                order.coupon = getCoupon(req,code)
                order.save()
                #msg: coupon added successfully
            return redirect("cart")
        else:
            #msg: coupon invalid
            return redirect("cart")
    else:
        #msg: Please enter a valid coupon
        return redirect("cart")


def removeCoupon(req):
    
    order = Order.objects.get(user=req.user,ordered=False)
    order.coupon = None
    order.save()
    return redirect("cart")







def makepayment(req):
    if req.method == "POST":
        address_id = req.POST.get("address")

        address = Address.objects.get(user = req.user,id=address_id)


        order = Order.objects.get(user=req.user,ordered=False)
        orderItems = order.items.all()

        orderItems.update(ordered=True)

        for item in orderItems:
            item.save()

        order.ordered  = True
        order.ref_code = get_ref_code(8)
        order.address = address
        order.save()
        send(req, address.contact, "Hi %s, Your Order placed successfully thanks for shopping with us " % address.name )

        return redirect('home')


def myOrder(req):
    order = Order.objects.filter(user=req.user,ordered=True)
    data = {
        "order":order
    }


    return render(req, 'public/my-order.html',data)
    








# def footer(request):
    # data = {"item":Item.objects.all(),"cat":Category.objects.all()}
    # return render(request,"public/footer.html")

