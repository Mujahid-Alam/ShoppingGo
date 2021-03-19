from django.contrib import admin
from ecom.models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Coupon)
admin.site.register(Order)