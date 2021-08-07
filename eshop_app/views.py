from hashlib import new
import random
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from eShop.settings import *
from PayTm import checksum
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from datetime import datetime
    
def home(request):
    url = "home"
    return render(request, 'home.html', {'url' : url})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        data = {
            'email' : email
        }

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                request.session['user'] = user.id
                auth.login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Wrong Password!!')
                return render(request, 'login.html', data)
        except:
            messages.info(request, 'Email is Not Registered!!')
            return render(request, 'login.html', data)
    else:
        return render(request, 'login.html')

def create_otp():
    no = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    otp = ""
    for i in range(6):
        otp += str(random.choice(no))
        print(otp)
    return otp

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        mobile = request.POST['mobile']
        password = request.POST['password']
        confirm_password = request.POST['confirm password']

        SpecialSym =['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']

        data = {
            'first_name' : first_name,
            'last_name' : last_name,
            'email' : email,
            'username' : username,
            'mobile' : mobile
        }

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already taken!!')
            return render(request, 'signup.html', data)
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken!!')
            return render(request, 'signup.html', data)
        elif Profile.objects.filter(mobile=mobile).exists():
            messages.info(request, 'Mobile Number already taken!!')
            return render(request, 'signup.html', data)
        elif len(mobile)<10 or len(mobile)>10:
            messages.info(request, 'Mobile Number Should be 10 characters!!')
            return render(request, 'signup.html', data)
        elif len(password) < 8:
            messages.info(request, 'Password Should Have at least 8 Characters!!')
            return render(request, 'signup.html', data)
        elif not any(char.isdigit() for char in password):
            messages.info(request, 'Password Should Have at least 8 Characters, at least One Number, at least One Uppercase Letter, at least One Lowercase Letter and at least One Special Character!!')
            return render(request, 'signup.html', data)
        elif not any(char.isupper() for char in password):
            messages.info(request, 'Password Should Have at least 8 Characters, at least One Number, at least One Uppercase Letter, at least One Lowercase Letter and at least One Special Character!!')
            return render(request, 'signup.html', data)
        elif not any(char.islower() for char in password):
            messages.info(request, 'Password Should Have at least 8 Characters, at least One Number, at least One Uppercase Letter, at least One Lowercase Letter and at least One Special Character!!')
            return render(request, 'signup.html', data)
        elif not any(char in SpecialSym for char in password):
            messages.info(request, 'Password Should Have at least 8 Characters, at least One Number, at least One Uppercase Letter, at least One Lowercase Letter and at least One Special Character!!')
            return render(request, 'signup.html', data)
        elif password == confirm_password:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
            profile = Profile(user=user, mobile=mobile)

            #email sent
            otp = create_otp()
            subject = 'Eshop India Company'
            message = f"Your OTP for Verification is-{otp}.\n\nNote:- Don't share your OTP with anyone.\n\nFrom:- Eshop India Company"
            email_from = settings.EMAIL_HOST_USER
            email_to = email

            #send_mail('subject', 'body', 'sender mail', 'receiver mail')
            send_mail(subject, message, email_from, [email_to], fail_silently=False)

            #user save
            profile.save()
            user.save()

            #session
            request.session['otp'] = otp
                
            return redirect('otpcheck')
        else:
            messages.info(request, 'Password and Confirm Password not matched!!')
            return render(request, 'signup.html', data)
    else:
        return render(request, 'signup.html')

def otpcheck(request):
    if 'otp' in request.session.keys():
        if request.method == 'POST':
            otp = request.POST['otp']
            if request.session['otp'] == otp:
                del request.session['otp']
                return redirect('login')
            else:
                messages.info(request, 'OTP is Invalid')
                return render(request, 'otp_check.html')
        return render(request, 'otp_check.html')
    else:
        return redirect('signup')

@login_required(login_url="/login")
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url="/login")
def profile(request):
    url = "profile"
    update_status = False
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = User.objects.get(id = int(request.user.id))
            profile = Profile.objects.get(user = user)
            first_name = request.POST.get('first_name')
            last_name = request.POST['last_name']
            username = request.POST['username']
            mobile = request.POST['mobile']

            if username!=user.username: 
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username is associated with another account!!')
                    return render(request, 'profile.html', {'url' : url})
            if mobile!=profile.mobile:
                if Profile.objects.filter(mobile=mobile).exists():
                    messages.info(request, 'Mobile is associated with another account!!')
                    return render(request, 'profile.html', {'url' : url})
                elif len(mobile)<10 or len(mobile)>10:
                    messages.info(request, 'Mobile Number Should be 10 characters!!')
                    return render(request, 'profile.html', {'url' : url})

            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            profile.mobile = mobile

            user.save()
            profile.save()
            update_status = True
        return render(request, 'profile.html', {'url' : url, 'update_status' : update_status})
    else:
        return render(request, 'login.html', {'url':url})

@login_required(login_url="/login")
def address(request):
    url = "profile"
    if request.user.is_authenticated:
        user = User.objects.get(id = int(request.user.id))
        addresses = [add for add in Address.objects.all() if add.user == user]

        return render(request, 'address.html', {'addresses' : addresses, 'url' : url})
    
@login_required(login_url="/login")
def add_address(request):
    url = "profile"
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = User.objects.get(id = int(request.user.id))

            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']
            pin_code = request.POST['pin_code']

            addresses = Address(user = user, address = address, city = city, state = state, country = country, pin_code = pin_code)
            addresses.save()
            return redirect('address')
        else:
            return render(request, 'add_address.html', {'url' : url})

@login_required(login_url="/login")
def edit_address(request, id):
    url = "profile"
    addresses = Address.objects.get(id=id)
    return render(request, 'edit_address.html', {'addresses' : addresses, 'add_id' : id, 'url' : url})

@login_required(login_url="/login")
def edit_address_form(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            add_id = request.POST['add_id']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']
            pin_code = request.POST['pin_code']

            addresses = Address.objects.get(id=add_id)

            addresses.address = address
            addresses.city = city
            addresses.state = state
            addresses.country = country
            addresses.pin_code = pin_code
            addresses.save()
            return redirect('address')

def remove_address(request):
    if request.method == 'GET':
        add_id = request.GET.get("add_id")
        address = Address.objects.get(Q(id=add_id) & Q(user=request.user))
        address.delete()
        msg = 'Address is removed successfully'
        
        return JsonResponse({'msg' : msg})

@login_required(login_url="/login")
def change_password(request):
    url = "profile"
    if request.method == 'POST':
        SpecialSym =['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        user = request.user

        old_pass = request.POST['old_password']
        new_pass = request.POST['new_password']
        confirm_pass = request.POST['confirm_password']
        
        if user.check_password(old_pass):
            if len(new_pass) < 8:
                messages.info(request, 'Password Should Have at least 8 Characters!!')
                return render(request, 'change_password.html', {'url' : url})
            elif not any(char.isdigit() for char in new_pass):
                messages.info(request, 'Password Should Have at least 8 Characters, at least One Number, at least One Uppercase Letter, at least One Lowercase Letter and at least One Special Character!!')
                return render(request, 'change_password.html', {'url' : url})
            elif not any(char.isupper() for char in new_pass):
                messages.info(request, 'Password Should Have at least 8 Characters, at least One Number, at least One Uppercase Letter, at least One Lowercase Letter and at least One Special Character!!')
                return render(request, 'change_password.html', {'url' : url})
            elif not any(char.islower() for char in new_pass):
                messages.info(request, 'Password Should Have at least 8 Characters, at least One Number, at least One Uppercase Letter, at least One Lowercase Letter and at least One Special Character!!')
                return render(request, 'change_password.html', {'url' : url})
            elif not any(char in SpecialSym for char in new_pass):
                messages.info(request, 'Password Should Have at least 8 Characters, at least One Number, at least One Uppercase Letter, at least One Lowercase Letter and at least One Special Character!!')
                return render(request, 'change_password.html', {'url' : url})
            elif new_pass == confirm_pass:
                user.password = make_password(new_pass)
                user.save()
                change_status = True
                return render(request, 'login.html', {'change_status' : change_status})
            else:
                messages.info(request, 'Password and Confirm Password not matched!!')
                return render(request, 'change_password.html', {'url' : url})
        
        else:
            messages.info(request, 'Old Password is Incorrect!!')
            return render(request, 'change_password.html', {'url' : url})
    return render(request, 'change_password.html', {'url' : url})

def forget_password(request):
    url = "profile"
    return render(request, 'forget_password.html', {'url' : url})

def forget_password_email_form(request):
    url = "profile"
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            #email sent
            otp = create_otp()
            subject = 'Eshop India Company'
            message = f"Your OTP for Verification is-{otp}.\n\nNote:- Don't share your OTP with anyone.\n\nFrom:- Eshop India Company"
            email_from = settings.EMAIL_HOST_USER
            email_to = email

            #send_mail('subject', 'body', 'sender mail', 'receiver mail')
            send_mail(subject, message, email_from, [email_to], fail_silently=False)

            #session
            request.session['otp'] = otp
            return render(request, 'forget_password_form.html', {'url' : url, 'email' : email})
        else:
            messages.info(request, 'Email is Not Registered Yet!!')
            return render(request, 'forget_password.html', {'url' : url, 'email' : email})
    else:
        return render(request, 'forget_password.html', {'url' : url})

def forget_password_form(request):
    url = "profile"
    if 'otp' in request.session.keys():
        if request.method == 'POST':
            SpecialSym =['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']  

            email = request.POST['email']
            new_pass = request.POST['new_pass']
            confirm_pass = request.POST['confirm_pass']
            otp = request.POST['otp']

            if request.session['otp'] == otp:
                if len(new_pass) < 8:
                    messages.info(request, 'Password Should Have at least 8 Characters!!')
                    return render(request, 'forget_password_form.html', {'url' : url, 'otp' : otp, 'email' : email})
                elif not any(char.isdigit() for char in new_pass):
                    messages.info(request, 'Password Should Have at least 8 Characters, at least One Number, at least One Uppercase Letter, at least One Lowercase Letter and at least One Special Character!!')
                    return render(request, 'forget_password_form.html', {'url' : url, 'otp' : otp, 'email' : email})
                elif not any(char.isupper() for char in new_pass):
                    messages.info(request, 'Password Should Have at least 8 Characters, at least One Number, at least One Uppercase Letter, at least One Lowercase Letter and at least One Special Character!!')
                    return render(request, 'forget_password_form.html', {'url' : url, 'otp' : otp, 'email' : email})
                elif not any(char.islower() for char in new_pass):
                    messages.info(request, 'Password Should Have at least 8 Characters, at least One Number, at least One Uppercase Letter, at least One Lowercase Letter and at least One Special Character!!')
                    return render(request, 'forget_password_form.html', {'url' : url, 'otp' : otp, 'email' : email})
                elif not any(char in SpecialSym for char in new_pass):
                    messages.info(request, 'Password Should Have at least 8 Characters, at least One Number, at least One Uppercase Letter, at least One Lowercase Letter and at least One Special Character!!')
                    return render(request, 'forget_password_form.html', {'url' : url, 'otp' : otp, 'email' : email})
                elif new_pass == confirm_pass:
                    del request.session['otp']

                    user = User.objects.get(email=email)
                    user.password = make_password(new_pass)
                    user.save()
                    change_status = True
                    return render(request, 'login.html', {'change_status' : change_status})
                else:
                    messages.info(request, 'Password and Confirm Password not matched!!')
                    return render(request, 'forget_password_form.html', {'url' : url, 'otp' : otp, 'email' : email})

            else:
                messages.info(request, 'OTP is Invalid')
                return render(request, 'forget_password_form.html', {'url' : url, 'otp' : otp, 'email' : email})    
    else:
        return render(request, 'forget_password_form.html', {'url' : url})

def searchMatch(search, product):
    if search in product.product_name.lower() or search in product.category.name.lower():
        return True
    else: 
        return False

def search(request):
    search = request.GET.get('search')
    product_list = Product.objects.all()
    products = [pro for pro in product_list if searchMatch(search.lower(), pro)]
    if len(products) == 0:
        return render(request, 'nosearch.html')
    else:
        return render(request, 'shop.html', {'products' : products})

def shop(request):
    url = "shop"
    return render(request, 'shop.html', {'url' : url})
    
def shopbycategory(request, catid):
    url = "shop"
    products = Product.objects.filter(category=catid)
    
    context = {
        'products' : products, 
        'url' : url
    }
    return render(request, 'shop.html', context)

def shopbysubcategory(request, catid, subid):
    url = "shop"
    products = Product.objects.filter(Q(category=catid) & Q(sub_category=subid))
    
    context = {
       'products' : products, 
       'url' : url
    }

    return render(request, 'shop.html', context)

def product(request, id):
    url = "shop"
    products = Product.objects.filter(id=id)
    return render(request, 'product.html', {'products' : products, 'url' : url})

@login_required(login_url="/login")
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id')
        print(product_id)
        quantity = request.POST.get('quantity')
        product = Product.objects.get(id = product_id)
        if Cart.objects.filter(product=product).exists():
            cart = Cart.objects.get(product=product)
            cart.quantity = cart.quantity + int(quantity)
            cart.save()
        else:
            Cart(user=user, product=product, quantity=quantity).save()
        return redirect('/cart')

@login_required(login_url="/login")
def cart(request):
    url = "shop"
    if User.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0
        shipping_amount = 0
        total_amount = 0
        cart_product = [pro for pro in Cart.objects.all() if pro.user == user]
        
        if cart_product:
            for pro in cart_product:
                product_amount = (pro.quantity * pro.product.product_price)
                amount += product_amount
                if amount < 500:
                    shipping_amount = 70
                    total_amount = amount + shipping_amount
                else:
                    shipping_amount = 0
                    total_amount = amount

            context = {
                'carts' : cart,
                'shipping_amount' : shipping_amount,
                'amount' : amount,
                'total_amount' : total_amount, 
                'url' : url
            }
            return render(request, 'cart.html', context)
        else:
            return render(request, 'emptycart.html', {'url':url})

def pluscart(request):
    if request.method == 'GET':
        prod_id = request.GET.get("prod_id")
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        product = Product.objects.get(id=prod_id)
        product_price = product.product_price
        cart.quantity += 1
        cart.save()
        
        amount = 0
        shipping_amount = 0
        total_amount = 0
        cart_product = [pro for pro in Cart.objects.all() if pro.user == request.user]

        for pro in cart_product:
            product_amount = (pro.quantity * pro.product.product_price)
            amount += product_amount
            if amount < 500:
                shipping_amount = 70
                total_amount = amount + shipping_amount
            else:
                shipping_amount = 0
                total_amount = amount
        context = {
            'quantity' : cart.quantity,
            'shipping_amount' : shipping_amount,
            'amount' : amount,
            'total_amount' : total_amount,
            'product_price' : product_price
        }
        return JsonResponse(context)

def minuscart(request):
    if request.method == 'GET':
        prod_id = request.GET.get("prod_id")
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        product = Product.objects.get(id=prod_id)
        product_price = product.product_price
        if cart.quantity > 1 :
            cart.quantity -= 1
        cart.save()
        
        amount = 0
        shipping_amount = 0
        total_amount = 0
        cart_product = [pro for pro in Cart.objects.all() if pro.user == request.user]

        for pro in cart_product:
            product_amount = (pro.quantity * pro.product.product_price)
            amount += product_amount
            if amount < 500:
                shipping_amount = 70
                total_amount = amount + shipping_amount
            else:
                shipping_amount = 0
                total_amount = amount
        context = {
            'quantity' : cart.quantity,
            'shipping_amount' : shipping_amount,
            'amount' : amount,
            'total_amount' : total_amount,
            'product_price' : product_price
        }
        return JsonResponse(context)

def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET.get("prod_id")
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.delete()
        
        amount = 0
        shipping_amount = 0
        total_amount = 0
        cart_product = [pro for pro in Cart.objects.all() if pro.user == request.user]

        for pro in cart_product:
            product_amount = (pro.quantity * pro.product.product_price)
            amount += product_amount
            if amount < 500:
                shipping_amount = 70
                total_amount = amount + shipping_amount
            else:
                shipping_amount = 0
                total_amount = amount
        cart_product = [pro for pro in Cart.objects.all() if pro.user == request.user]
        product_count = len(cart_product)

        context = {
            'shipping_amount' : shipping_amount,
            'amount' : amount,
            'total_amount' : total_amount,
            'product_count' : product_count,
        }
        return JsonResponse(context)

@login_required(login_url="/login")
def checkout(request):
    url = "shop"
    if request.user.is_authenticated:
        user = User.objects.get(id = int(request.user.id))
        addresses = [add for add in Address.objects.all() if add.user == user]

        cart_items = Cart.objects.filter(user=user)
        amount = 0
        shipping_amount = 0
        total_amount = 0
        cart_product = [pro for pro in Cart.objects.all() if pro.user == request.user]

        if cart_product:
            for pro in cart_product:
                product_amount = (pro.quantity * pro.product.product_price)
                amount += product_amount
                if amount < 500:
                    shipping_amount = 70
                    total_amount = amount + shipping_amount
                else:
                    shipping_amount = 0
                    total_amount = amount

        context = {
            'addresses' : addresses, 
            'cart_items' : cart_items,
            'shipping_amount' : shipping_amount,
            'amount' : amount,
            'total_amount' : total_amount,
            'url' : url
        }
        return render(request, 'check-out.html', context)

@login_required(login_url="/login")
def payment(request):
    url = "shop"
    if request.method == 'POST':
        amount = request.POST['amount']
        shipping_amount = request.POST['shipping_amount']
        total_amount = request.POST['total_amount']
        add_id = request.POST['add_id']
        
        oid = random.randint(0, 10000000)
        order_id = "order" + str(oid)
        add = Address.objects.get(id=add_id)
        carts = Cart.objects.filter(user= request.user)
        if request.POST.get('cod'):
            for cart_item in carts:
                order = Order(user=request.user, order_id=order_id, product=cart_item.product, quantity=cart_item.quantity, amount=amount, shipping_amount=shipping_amount, total_amount=total_amount, address=add.address, city=add.city, state=add.state, country=add.country, pin_code=add.pin_code, payment_mode='COD', payment_status=False)
                order.save()
                Payment(user=order.user, order=order, orderid=order_id, payment_mode='COD', payment_status=False, payment_through='None', bank_name='None').save()
                cart_item.delete()
            return  render(request, 'cod.html', {'order_id' : order_id, 'url':url})

        elif request.POST.get('online'):
            for cart_item in carts:
                order = Order(user=request.user, order_id=order_id, product=cart_item.product, quantity=cart_item.quantity, amount=amount, shipping_amount=shipping_amount, total_amount=total_amount, address=add.address, city=add.city, state=add.state, country=add.country, pin_code=add.pin_code)
                order.save()
            param_dict={
                'MID': settings.MERCHANT_MID,
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(total_amount),
                'CUST_ID': 'eshop.india.company@gmail.com',
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'https://eshopindia.herokuapp.com/payment_status',
            }
            param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, settings.MERCHANT_KEY)
            return  render(request, 'paytm.html', {'param_dict': param_dict, 'url' : url})
    return render(request, 'check-out.html', {'url' : url})
    
@csrf_exempt
def payment_status(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            Checksum = form[i]

    verify = checksum.verify_checksum(response_dict, settings.MERCHANT_KEY, Checksum)
    order_id = str(response_dict['ORDERID'])
    orders = [order for order in Order.objects.all() if order.order_id == order_id]

    if verify:
        if response_dict['RESPCODE'] == '01':
            for order in orders:
                order.payment_status = True
                order.save()
                if response_dict['PAYMENTMODE'] == 'PPI':
                    payment_through = 'Paytm Wallet'
                elif response_dict['PAYMENTMODE'] == 'CC':
                    payment_through = 'Credit Card'
                elif response_dict['PAYMENTMODE'] == 'DC':
                    payment_through = 'Debit Card'
                elif response_dict['PAYMENTMODE'] == 'NB':
                    payment_through = 'Net Banking'
                bank_name = response_dict['BANKNAME']
                Payment(user=order.user, order=order, orderid=order_id, payment_status=True, payment_through=payment_through, bank_name=bank_name).save()
                carts = Cart.objects.filter(user = order.user)
                for cart_item in carts:
                    cart_item.delete()
                
        else:
            for order in orders:
                order.delete()
    return render(request, 'paymentstatus.html', {'response': response_dict})

@login_required(login_url="/login")
def order(request):
    url = "order"
    orders = [order for order in Order.objects.all() if order.user == request.user]
    order_id = []
    if orders:
        for order in orders:
            order_id.append(order.order_id)
        order_id = list(dict.fromkeys(order_id))
        return render(request, 'orders.html', {'orders':orders, 'order_id' : order_id, 'url' : url})
    else:
        return render(request, 'noorder.html', {'url':url})

@login_required(login_url="/login")
def order_details(request, id):
    url = "order"
    orders = Order.objects.filter(order_id = id)
    payments = Payment.objects.filter(orderid = id)
    for order in orders:
        order_id = order.order_id
        order_date = order.order_date
        amount = order.amount
        shipping_amount = order.shipping_amount
        total_amount = order.total_amount
        order_address = order.address
        order_city = order.city
        order_state = order.state
        order_country = order.country
        order_pin_code = order.pin_code
        payment_mode = order.payment_mode
        payment_status = order.payment_status
        order_status = order.order_status
        delivery_date = order.delivery_date
    for payment in payments:
        payment_through = payment.payment_through
        bank_name = payment.bank_name
    context = {
        'orders' : orders, 
        'order_id' : order_id, 
        'order_date' : order_date, 
        'amount' :amount,
        'shipping_amount' : shipping_amount,
        'total_amount' : total_amount,
        'order_address' : order_address,
        'order_city' : order_city,
        'order_state' : order_state,
        'order_country' : order_country,
        'order_pin_code' : order_pin_code,
        'payment_mode' : payment_mode,
        'payment_status' : payment_status,
        'payment_through' : payment_through,
        'bank_name' : bank_name,
        'order_status' : order_status, 
        'delivery_date' : delivery_date,
        'url' : url
    }
    return render(request, 'order_details.html', context)       

def cancel_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        print(order_id)
        orders = Order.objects.filter(order_id=order_id)  
        for order in orders:
            order.order_status = 'Cancel'
            order.delivery_date = datetime.now()
            order.save()

        return redirect('order')

def contact(request):
    url = "contact"
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        Contact(name=name, email=email, message=message).save()
        status = True
        return render(request, 'contact.html', {'status' : status, 'url' : url})
    else:
        return render(request, 'contact.html', {'url' : url})
