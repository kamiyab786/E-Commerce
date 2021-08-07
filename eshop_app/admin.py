from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import *

# Register your models here.

@admin.register(Header)
class AdminCategory(admin.ModelAdmin):
    list_display = ['email', 'phone', 'address']

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Sub_Category)
class AdminSubCategory(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']

@admin.register(Hero)
class AdminCategory(admin.ModelAdmin):
    list_display = ['hero_title', 'hero_header', 'hero_headline']

@admin.register(Banner)
class AdminCategory(admin.ModelAdmin):
    list_display = ['banner_title']

@admin.register(Slider)
class AdminCategory(admin.ModelAdmin):
    list_display = ['slider_title', 'category']

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'category', 'sub_category', 'product_price']

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ['user', 'mobile']

@admin.register(Address)
class AdminAddress(admin.ModelAdmin):
    list_display = ['user', 'address', 'city', 'state', 'country', 'pin_code']

@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['user', 'product_info', 'quantity'] 

    def product_info(self, obj):
        link = reverse("admin:eshop_app_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', link, obj.product.product_name)

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['user', 'order_id', 'product_info', 'quantity', 'amount', 'shipping_amount', 'total_amount', 'address', 'city', 'state', 'country', 'pin_code', 'order_date', 'payment_mode', 'payment_status', 'order_status', 'delivery_date']

    def product_info(self, obj):
        link = reverse("admin:eshop_app_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', link, obj.product.product_name)

@admin.register(Payment)
class AdminPayment(admin.ModelAdmin):
    list_display = ['user', 'order_id', 'payment_mode', 'payment_status', 'payment_through', 'bank_name']

    def order_id(self, obj):
        link = reverse("admin:eshop_app_order_change", args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', link, obj.order.order_id)

@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']