
from django.contrib import admin
from django.urls import path,include

from ecom.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    path('',homepages,name="home"),
    path('accounts/', include('allauth.urls')),
    path('product/<str:slug>/',productView,name="product"),
    path('cat/<str:cat_slug>/',categoryView,name="cat"),
    path('search/',searchView,name="search"),
    path('cart/',orderSummery,name="cart"),
    path('checkout/',checkout,name="checkout"),
    path('my-order/',myOrder,name="myOrder"),
    path('add-coupon/',addCoupon,name="addCoupon"),
    path('remove-coupon/',removeCoupon,name="removeCoupon"),
    path('make-payment/',makepayment,name="makePayment"),
    path('add-to-cart/<str:slug>/',addTocart,name="add-to-cart"),
    path('remove-from-cart/<str:slug>/',remove_from_cart_single,name="remove-from-cart"),

   


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
