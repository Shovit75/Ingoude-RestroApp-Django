from django.shortcuts import redirect, render
from .models import Food, Category, WebUser, Checkout, Chef
from decimal import Decimal
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.\

def sessions(request):
    sessions = Session.objects.all()
    return render(request, "restro/sessions.html",{
        'session': sessions
    })

def index(request):
    food = Food.objects.filter(featured=True)
    featuredcat = Category.objects.filter(featured=True)
    featuredchef = Chef.objects.filter(featured=True)
    category = Category.objects.all()
    if request.session.get('cart'):
        cartcount = sum(item['item_quantity'] for item in request.session['cart'])
    else:
        cartcount = 0
    return render(request, "restro/index.html", {
        'foods' : food,
        'cat' : category,
        'featuredcat': featuredcat,
        'featuredchefs' : featuredchef,
        'cartcount' : cartcount
    })

def food(request, food_id):
    food = Food.objects.get(id = food_id)
    category = Category.objects.all()
    if request.session.get('cart'):
        cartcount = sum(item['item_quantity'] for item in request.session['cart'])
    else:
        cartcount = 0
    return render(request, "restro/food.html", {
        'food' : food,
        'cat' : category,
        'cartcount': cartcount
    })

def category(request, category_id):
    categories = Category.objects.get(id = category_id)
    foods = categories.foods.all()
    category = Category.objects.all()
    if request.session.get('cart'):
        cartcount = sum(item['item_quantity'] for item in request.session['cart'])
    else:
        cartcount = 0
    return render(request, "restro/category.html", {
        "category" : categories,
        "items" : foods,
        "cat": category,
        'cartcount': cartcount
    })

def webuserlogin(request):
    category = Category.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = WebUser.objects.get(username=username)
            if user.check_password(password):
                # Manually handle the session
                request.session['webuser_id'] = user.id
                request.session['webuser_username'] = user.username
                return redirect('index')
            else:
                return render(request, "restro/login.html", {
                    "cat": category,
                    "error": "Invalid credentials"
                })
        except WebUser.DoesNotExist:
            return render(request, "restro/login.html", {
                "cat": category,
                "error": "Invalid credentials"
            })
    return render(request, "restro/login.html",{
        "cat": category
    })

def webuserregister(request):
    category = Category.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            return render(request, "restro/register.html", {
                "cat": category,
                "error": "Username and password are required"
            })
        
        if WebUser.objects.filter(username=username).exists():
            return render(request, "restro/register.html", {
                "cat": category,
                "error": "Username already exists"
            })

        if len(password) < 8:  # Example of password length validation
            return render(request, "restro/register.html", {
                "cat": category,
                "error": "Password must be at least 8 characters long"
            })
        
        user = WebUser(username=username)
        user.set_password(password)
        user.save()
        return redirect('webuserlogin')  
    return render(request, "restro/register.html",{
        "cat": category
    })

def webuserlogout(request):
    request.session.flush()
    return redirect('index')

def addtocart(request, item_slug, item_name, item_price):
    if 'cart' not in request.session:
        request.session['cart'] = []
    if 'item_id_counter' not in request.session:
        request.session['item_id_counter'] = 0
    itemfound = False
    for item in request.session['cart']:
        if item['item_slug'] == item_slug:
            itemfound = True
            item['item_quantity'] += 1
            request.session.modified = True
            break
    if not itemfound:
        request.session['item_id_counter'] += 1
        cart_item = {
            'item_slug': item_slug,
            'item_id': request.session['item_id_counter'],
            'item_name': item_name,
            'item_price': str(item_price),
            'item_quantity': 1
        }
        request.session['cart'].append(cart_item)
        request.session.modified = True
        messages.success(request, 'Item has been added successfully.')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'Item has been added successfully.')
    return redirect(request.META.get('HTTP_REFERER', 'index'))
        
def cart(request):
    cartitems = request.session.get('cart', [])
    total_items = sum(Decimal(item['item_quantity']) for item in cartitems)
    total_price = sum(Decimal(item['item_quantity']) * Decimal(item['item_price']) for item in cartitems)
    category = Category.objects.all()
    if request.session.get('cart'):
        cartcount = sum(item['item_quantity'] for item in request.session['cart'])
    else:
        cartcount = 0
    return render(request, "restro/cart.html",{
        "cartitems" : cartitems,
        "totalitems" : total_items,
        "totalprice" : total_price,
        "cat": category,
        "cartcount" : cartcount
    })

def clearcart(request):
    request.session.pop('cart', None)
    request.session.pop('item_id_counter', None)
    return redirect(request.META.get('HTTP_REFERER'))

def deleteitem(request, item_id):
    cart = request.session.get('cart', [])
    item_found = False
    for item in cart:
        if item['item_id'] == item_id:
            item_found = True
            if item['item_quantity'] > 1:
                item['item_quantity'] -= 1
            else:
                cart = [i for i in cart if i['item_id'] != item_id]
                break
    if item_found:
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'Item deleted successfully.')
    else:
        messages.success(request, 'Item not found in cart.')
    return redirect(request.META.get('HTTP_REFERER'))

def checkout(request):
    if request.method == "POST":
        username = request.POST['username']
        address = request.POST['address']
        phone = request.POST['phone']
        if not username or not address or not phone:
            messages.success(request, 'Address and Phone is required.')
            return redirect(request.META.get('HTTP_REFERER'))
        if len(phone) != 10 or not phone.isdigit():
            messages.success(request, 'Phone must be 10 digits')
            return redirect(request.META.get('HTTP_REFERER'))
        if phone[0] not in '789':
            messages.success(request, 'Invalid Phone Number')
            return redirect(request.META.get('HTTP_REFERER'))
        # create modal flag and store address and phone
        request.session['flag'] = True
        request.session['address'] = address
        request.session['phone'] = phone
        cartitems = request.session.get('cart', [])
        flag = request.session.get('flag')
        addr = request.session.get('address')
        phn = request.session.get('phone')
        category = Category.objects.all()
        total_items = sum(Decimal(item['item_quantity']) for item in cartitems)
        total_price = sum(Decimal(item['item_quantity']) * Decimal(item['item_price']) for item in cartitems)
        if request.session.get('cart'):
            cartcount = sum(item['item_quantity'] for item in request.session['cart'])
        else:
            cartcount = 0
        return render(request, "restro/checkout.html", {
            "cartitems" : cartitems,
            "totalitems" : total_items,
            "totalprice" : total_price,
            "cat": category,
            "cartcount" : cartcount,
            'flag' : flag,
            "address": addr,
            "phone" : phn
        })
    cartitems = request.session.get('cart', [])
    category = Category.objects.all()
    total_items = sum(Decimal(item['item_quantity']) for item in cartitems)
    total_price = sum(Decimal(item['item_quantity']) * Decimal(item['item_price']) for item in cartitems)
    if request.session.get('cart'):
        cartcount = sum(item['item_quantity'] for item in request.session['cart'])
    else:
        cartcount = 0
    # Remove the flag, address and phone from the session
    request.session.pop('flag', False)
    request.session.pop('address', None)
    request.session.pop('phone', None)
    return render(request, "restro/checkout.html", {
        "cartitems" : cartitems,
        "totalitems" : total_items,
        "totalprice" : total_price,
        "cat": category,
        "cartcount" : cartcount
    })

def completetransaction(request):
    if request.method == 'POST':
        # Process the received data as needed. Example: Save transaction details to the database
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        username = request.session.get('webuser_username')
        order = request.session.get('cart', [])
        total_price = sum(Decimal(item['item_quantity']) * Decimal(item['item_price']) for item in order)
        checkout = Checkout(
            username=username,
            address=address,
            phone=phone,
            price=total_price
        )
        checkout.set_order(order)
        checkout.save()
        request.session.pop('flag', False)
        request.session.pop('address', None)
        request.session.pop('phone', None)
        request.session.pop('cart', None)
        request.session.pop('item_id_counter', None)
        messages.success(request, 'Checkout Completed.')
        return JsonResponse({'status': 'success', 'message': 'Transaction recorded'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)