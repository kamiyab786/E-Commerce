from .models import *

def extra(request):
    cart_product = [pro for pro in Cart.objects.all() if pro.user == request.user]
    product_count = len(cart_product)

    headers = Header.objects.all()
    categories = Category.objects.all()
    sub_categories = Sub_Category.objects.all()
    heros = Hero.objects.all()
    banners = Banner.objects.all()
    sliders = Slider.objects.all()
    products = Product.objects.all()    

    context = {
        'product_count' : product_count,
        'headers' : headers,
        'categories' : categories,
        'sub_categories' : sub_categories,
        'heros' :heros,
        'banners' : banners,
        'sliders' : sliders,
        'products' : products
    }
    return context