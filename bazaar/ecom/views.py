from django.shortcuts import render,get_object_or_404,redirect
from ecom.models import *






# from django.utils import timezone
from django.utils import timezone







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
                return redirect(orderSummery)
        else:
            #todo msg: this item is not availabble in your cart
            return redirect(orderSummery)
    else:
        #todo msg: you not have in active order
        return redirect(orderSummery)



def orderSummery(req):
    order = Order.objects.get(user=req.user,ordered=False)
    data = {"order": order}

    return render(req, "public/cart.html",data)


