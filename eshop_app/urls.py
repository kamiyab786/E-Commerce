from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('address', views.address, name='address'),
    path('add_address', views.add_address, name='add_address'),
    path('edit_address_form', views.edit_address_form, name='edit_address_form'),
    path('edit_address/<int:id>', views.edit_address, name='edit_address'),
    path('remove_address', views.remove_address, name='remove_address'),
    path('change_password', views.change_password, name='change_password'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('forget_password_email_form', views.forget_password_email_form, name='forget_password_email_form'),
    path('forget_password_form', views.forget_password_form, name='forget_password_form'),
    path('otpcheck', views.otpcheck, name='otpcheck'),
    path('search', views.search, name='search'),
    path('shop', views.shop, name='shop'),
    path('shop/<int:catid>', views.shopbycategory, name='shopbycategory'),
    path('shop/<int:catid>/<int:subid>', views.shopbysubcategory, name='shopbysubcategory'),
    path('product/<int:id>', views.product, name='product'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('pluscart', views.pluscart, name='pluscart'),
    path('minuscart', views.minuscart, name='minuscart'),
    path('removecart', views.removecart, name='removecart'),
    path('checkout', views.checkout, name='check-out'),
    path('payment', views.payment, name='payment'),
    path("payment_status", views.payment_status, name="payment_status"),
    path('order', views.order, name='order'),
    path('order_details/<slug:id>', views.order_details, name='order_details'),
    path('cancel_order', views.cancel_order, name='cancel_order'),
    path('contact', views.contact, name='contact'),
]
