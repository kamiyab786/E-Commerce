from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ("Men's Fashion", "Men's Fashion"),
    ("Women's Fashion", "Women's Fashion"),
    ("Kid's Fashion", "Kid's Fashion"),
    ("Mobiles & Electronics", "Mobiles & Electronics"),
    ("Home Appliances", "Home Appliances"),
    ("Grocery", "Grocery"),
)

SUB_CATEGORY_CHOICES = (
    ("Clothes", "Clothes"),
    ("Watches & Sunglasses", "Watches & Sunglasses"),
    ("Watches & Accessories", "Watches & Accessories"),
    ("Accessories", "Accessories"),
    ("Shoes", "Shoes"),
    ("Mobiles & Tablets", "Mobiles & Tablets"),
    ("Computers, Laptops & TV", "Computers, Laptops & TV"),
    ("Cameras & Audio", "Cameras & Audio"),
)

STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On The Way", "On The Way"),
    ("Delivered", "Delivered"),
    ("Cancel", "Cancel"),
    ("Rejected", "Rejected"),
)

PAYMENT_MODE_CHOICES = (
    ("COD", "COD"),
    ("Online", "online"),
)

# Nav Models
class Header(models.Model):
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    facebook = models.URLField(max_length=200)
    instagram = models.URLField(max_length=200)
    linkedin = models.URLField(max_length=200)
    github = models.URLField(max_length=200)
    logo = models.ImageField(upload_to='Header-images')
    favicon = models.ImageField(upload_to='Header-images')

# Category Models
class Category(models.Model):
    name = models.CharField(choices=CATEGORY_CHOICES, max_length=200)
    def __str__(self):
        return self.name

class Sub_Category(models.Model):
    name = models.CharField(choices=SUB_CATEGORY_CHOICES, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

# Home-Hero Models
class Hero(models.Model):
    hero_pic = models.ImageField(upload_to="Home-images")
    hero_title = models.CharField(max_length=100)
    hero_header = models.CharField(max_length=100)
    hero_headline = models.CharField(max_length=1000)

# Home-Banner Models
class Banner(models.Model):
    banner_pic = models.ImageField(upload_to="Home-images")
    banner_title = models.CharField(max_length=100)

# Home-Slider Models
class Slider(models.Model):
    large_pic = models.ImageField(upload_to="Home-images")
    slider_title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

# Product Models
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.IntegerField()
    description = models.TextField(max_length=1000)
    product_pic = models.ImageField(upload_to = 'Products')
    brand = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)

# Profile Models
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)

# Address Models
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    pin_code = models.IntegerField()

# Cart Models
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

# Order Models
class Order(models.Model):
    order_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.IntegerField()
    shipping_amount = models.IntegerField()
    total_amount = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    pin_code = models.IntegerField()
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE_CHOICES, default='Online')
    payment_status = models.BooleanField(default=False)
    order_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    delivery_date = models.DateTimeField(null=True)

# Payment Models
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    orderid = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE_CHOICES, default='Online')
    payment_status = models.BooleanField(default=False)
    payment_through = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=200)
    
# Contact Models
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=1000)