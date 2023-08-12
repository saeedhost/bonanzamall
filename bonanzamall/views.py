#Login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

#Model
from django.shortcuts import render, redirect
from ProductStore.models import Store_Product, Top_Product, Special_Offer, Comment
from CustomerOrders.models import CustomerBilling, CustomerBillingItem

import json
from django.http import JsonResponse
from django.shortcuts import redirect
from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum, Count

# from django.core.paginator import Paginator

from otp.models import OTP
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import IntegrityError
import random

# Stripe Payment APIs
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
import stripe 
# Assuming you have these constants defined somewhere in your project
FRONTEND_CHECKOUT_SUCCESS_URL = 'https://example.com/success'
FRONTEND_CHECKOUT_FAILED_URL = 'https://example.com/failed'

###########################(Login Registration START)###############################
def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP is: {otp}'
    from_email = 'khansaeed04717@gmail.com'  # Set your email address here or use a dedicated email account
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


def registration(request):
    if request.method == 'POST':
        email = request.POST.get('email2')
        username = request.POST.get('username2')
        password1 = request.POST.get('pass2')
        password2 = request.POST.get('cpass2')

        if ' ' in username:
            messages.error(request, "Username cannot contain spaces")
            return redirect('userReg') 
        
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('userReg')

        if len(username) < 3:
            messages.error(request, "Username must be at least 3 characters")
            return redirect('userReg')

        if len(username) > 16:
            messages.error(request, "Username must be less than 16 characters")
            return redirect('userReg')

        try:
            existing_user = User.objects.get(Q(username=username) | Q(email=email))
            if existing_user.username == username:
                messages.error(request, "An account already exists with this username")
            else:
                messages.error(request, "An account already exists with this email")
            return redirect('userReg')
        
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=email, password=password1)
            otp = generate_otp()  # Implement a function to generate a random 4-digit OTP
            final_otp = OTP.objects.create(user=user, otp=otp)
            final_otp.save()
            send_otp_email(email, otp)  # Implement a function to send the OTP to the user's email
            return render(request, 'verify_otp.html', {'email': email})
    else:
        return render(request, 'registration.html')


def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email2')
        otp = int(request.POST.get('otp'))

        users = User.objects.filter(email=email)

        print("User: ", users)

        if not users.exists():
            messages.error(request, "User not found")
            return redirect('verify_otp')

        print("User :",users)

        for user in users:
            try:
                otp_instance = OTP.objects.filter(user=user).latest('created_at')
                if otp == int(otp_instance.otp):
                    otp_instance.delete()
                    # Perform any other actions you want upon successful OTP verification
                    return redirect('Home')
            except OTP.DoesNotExist:
                pass

        messages.error(request, "Invalid OTP")
        return redirect('verify_otp')

    else:
        return render(request, 'verify_otp.html')

def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the username_or_email is an email
        if '@' in username_or_email:
            # Find the user by email
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                user = None
        else:
            # Find the user by username
            user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            try:
                otp_instance = OTP.objects.filter(user=user).latest('created_at')
                if otp_instance:
                    return render(request, 'verify_otp.html', {'email': user.email})
            except ObjectDoesNotExist:
                # Perform any other actions you want upon successful login
                login(request, user)
                return redirect('Home')

        messages.error(request, "Invalid username/email or password")
        return redirect('userLogin')
    else:
        return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    return redirect('userLogin')
###########################(Login Registration END)###############################

###########################(Header START)#########################################
def header(request):
    data = {}
    store_product = Store_Product.objects.order_by('?')[:6]
    data = {
        'store_product': store_product,
    }
    return render(request, "header.html", data)

###########################(Header END)###########################################

def home(request):
    data = {}
    # top_product = Top_Product.objects.order_by('?')[:3]
    top_product = Top_Product.objects.order_by('?')[:3]

    special_offer = Special_Offer.objects.order_by('?')[:2]
    store_product = Store_Product.objects.all()[:48]

    # Calculate Rating
    product_ids = store_product.values_list('id', flat=True)  
    product_ratings = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(Store_Product),
        object_id__in=product_ids
    ).values('object_id').annotate(
        total_rating=Sum('rating'),
        user_count=Count('user')
    )

    product_data = {}  # Dictionary to store product data

    for rating in product_ratings:
        product_id = rating['object_id']
        user_count = rating['user_count']
        total_rating = rating['total_rating']
        average_rating = round(total_rating / user_count, 1) if user_count > 0 else 0

        product_data[product_id] = {
            'average_rating': average_rating,
            'user_count': user_count
        }

    # Convert product_data to JSON
    product_data_json = json.dumps(product_data)

    data = {
        'top_product': top_product,
        'special_offer': special_offer,
        'store_product': store_product,
        'product_data_json': product_data_json,
    }

    return render(request, "index.html", data)

def shop(request):
    data={}
    searching_product = Store_Product.objects.all()
    special_offers = Special_Offer.objects.all()[:2]
    if request.method=="POST":
        search=request.POST.get('product_name')
        if search!=None:
            searching_product = Store_Product.objects.filter(product_name__icontains=search)

    # total_items_to_show= Paginator(searching_product, 40)  # two parameters. first one= what to show, second one= how many items to show
    # page_number=request.GET.get('page') # this will show in url like: home/?page=1
    # final_items=total_items_to_show.get_page(page_number)
    
    product_ids = searching_product.values_list('id', flat=True) 

    # Retrieve comments, ratings, and user counts for each store product
    product_ratings = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(Store_Product),
        object_id__in=product_ids
    ).values('object_id').annotate(
        total_rating=Sum('rating'),
        user_count=Count('user')
    )

    product_data = {}  # Dictionary to store product data
    for rating in product_ratings:
        product_id = rating['object_id']
        user_count = rating['user_count']

        # Calculate average rating for the product
        total_rating = rating['total_rating']
        average_rating = round(total_rating / user_count, 1) if user_count > 0 else 0

        product_data[product_id] = {
            'average_rating': average_rating,
            'user_count': user_count
        }

    # Convert product_data to JSON
    product_data_json = json.dumps(product_data)
    print(product_data_json)  # Print the JSON data

    data = {
        'searching_product':searching_product,
        'special_offers':special_offers,
        'product_data_json': product_data_json,
    }
    return render(request, "shop.html", data)

@login_required(login_url="/login/")
def contact(request):
    success=''
    failed=''
    data={}
    if request.method=="POST":
        subject=request.user.email
        user_email=request.POST.get('email')
        message=request.POST.get('message')

        if subject and user_email and message != '':
            send_mail(
                subject,
                message,
                user_email,
                ['saeed03644@gmail.com'],
                fail_silently=False,
            )
            success="Email Send successfully"
        else:
            failed="Email Sending failed...!"
        
    data={
        'success': success,
        'warning': failed,
    }
    return render(request, "contact.html", data)

@login_required(login_url="/login/")
def view_cart(request):
    return render(request, "cart.html")

@login_required(login_url="/login/")
def view_checkout(request):
    return render(request, "checkout.html")

###########################(Cart Start)###############################
@login_required(login_url="/login/")
def place_order(request):
    if request.method == 'POST':
        user = request.user
        
        billing = CustomerBilling.objects.create(
            user=user,
            fullname=request.POST.get('c_name'),
            email=request.POST.get('c_email'),
            province=request.POST.get('c_province'),
            district=request.POST.get('c_district'),
            mobile_number=request.POST.get('c_number'),
            address=request.POST.get('c_address')
        )

        cartItems = request.POST.getlist('itemSavingName')
        quantities = request.POST.getlist('itemSavingQty')
        total_prices = request.POST.getlist('savingTotalPrice')

        for i in range(len(cartItems)):
            item_name = cartItems[i]
            quantity = quantities[i]
            total_price = Decimal(total_prices[i])

            billing_item = CustomerBillingItem.objects.create(
                billing=billing,
                item_name=item_name,
                quantity=quantity,
                total_price=total_price,
            )
        messages.success(request, "Order placed Successfully")
        return redirect('Checkout')
    return render(request, "checkout.html")

@login_required(login_url="/login/")
def orders_history(request):
    user = request.user
    billings = CustomerBilling.objects.filter(user=user)

    context = {
        'billings': billings,
    }
    return render(request, 'order-history.html', context)

@login_required(login_url="/login/")
def order_details(request, invoice_number):
    user = request.user
    billing = CustomerBilling.objects.get(user=user, invoice_number=invoice_number)
   
    # Retrieve the related CustomerBillingItem objects
    items = billing.items.all()

    context = {
        'billing': billing,
        'items': items,
    }
    return render(request, 'order-details.html', context)

###########################(Cart End)###############################

#######################(Comment Section Start)######################

@login_required(login_url="/login/")
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
    comment.delete()

    return JsonResponse({'message': 'Comment has been deleted'})
###########################(Comment Section Closed)#################


###########################(checkout Start)###################################
"""class CreateCheckoutSession(APIView):
  def post(self, request):
    dataDict = dict(request.data)
    price = dataDict['price'][0]
    product_name = dataDict['product_name'][0]
    try:
      checkout_session = stripe.checkout.Session.create(
        line_items =[{
        'price_data' :{
          'currency' : 'usd',  
            'product_data': {
              'name': product_name,
            },
          'unit_amount': price
        },
        'quantity' : 1
      }],
        mode= 'payment',
        success_url= FRONTEND_CHECKOUT_SUCCESS_URL,
        cancel_url= FRONTEND_CHECKOUT_FAILED_URL,
        )
      return redirect(checkout_session.url , code=303)
    except Exception as e:
        print(e)
        return e
"""
###########################(checkout End)#####################################


###########################(Navbar Menus Start)###############################
def help(request):
    return render(request, "help.html")

def FAQ(request):
    return render(request, "FAQ.html")
def about(request):
    return render(request, "about.html")
###########################(Navbar Menus End)#################################


# ###########################(Product Details Started )#######################
def add_comment(request, product_details):
    products = Store_Product.objects.all()
    comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(product_details), object_id=product_details.pk)

    # Calculate Rating 
    product_ids = products.values_list('id', flat=True)  
    product_ratings = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(Store_Product),
        object_id__in=product_ids
    ).values('object_id').annotate(
        total_rating=Sum('rating'),
        user_count=Count('user')
    )

    product_data = {} 

    for rating in product_ratings:
        product_id = rating['object_id']
        user_count = rating['user_count']

        # Calculate average rating for the product
        total_rating = rating['total_rating']
        average_rating = round(total_rating / user_count, 1) if user_count > 0 else 0

        product_data[product_id] = {
            'average_rating': average_rating,
            'user_count': user_count
        }
    product_data_json = json.dumps(product_data)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            # User is not logged in, redirect to login page
            return redirect('/login/')

        rating = int(request.POST.get('rating'))
        content = request.POST.get('content')
        image = request.FILES.get('image')
        user = request.user
        # Check if the user has already commented on this product
        if Comment.objects.filter(user=user, content_type=ContentType.objects.get_for_model(product_details), object_id=product_details.pk).exists():
            messages.error(request, "You have already added a comment on this product.")
            data = {
                'products_details': product_details,
                'products': products,
                'comments': comments,
                'product_data_json': product_data_json,
            }
            return render(request, "all_products.html", data)

        comment = Comment(user=user, content_object=product_details, rating=rating, content=content, image=image)
        comment.save()

    data = {
        'products_details': product_details,
        'products': products,
        'comments': comments,
        'product_data_json': product_data_json,
    }
    return render(request, "all_products.html", data)

# ###########################(Product Details End)###############################


def top_products_details(request, top_products_name_ref):
    product_details = Top_Product.objects.get(slug_ref=top_products_name_ref)
    return add_comment(request, product_details)


def special_offers_details(request, special_offers_name_ref):
    product_details = Special_Offer.objects.get(slug_ref=special_offers_name_ref)
    return add_comment(request, product_details)


def store_products_details(request, store_products_name_ref):
    product_details = Store_Product.objects.get(slug_ref=store_products_name_ref)
    return add_comment(request, product_details)


############################# Sub Categories Start ##############################
def product_category(request, category_id):
    data={}
    all_items = Store_Product.objects.filter(product_category=category_id)

     # Calculate Rating 
    product_ids = all_items.values_list('id', flat=True)  
    product_ratings = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(Store_Product),
        object_id__in=product_ids
    ).values('object_id').annotate(
        total_rating=Sum('rating'),
        user_count=Count('user')
    )

    product_data = {} 

    for rating in product_ratings:
        product_id = rating['object_id']
        user_count = rating['user_count']

        # Calculate average rating for the product
        total_rating = rating['total_rating']
        average_rating = round(total_rating / user_count, 1) if user_count > 0 else 0

        product_data[product_id] = {
            'average_rating': average_rating,
            'user_count': user_count
        }
    product_data_json = json.dumps(product_data)

    data = {
        'all_items':all_items,
        'product_data_json': product_data_json,
    }
    return render(request, "product-category.html", data)

@login_required(login_url="/login/")
def product_category_details(request, all_products_name_ref):
    products_details= Store_Product.objects.get(slug_ref=all_products_name_ref)
    data={
        'products_details': products_details,
    }
    return render(request, "all_products.html", data)
############################# Sub Categories End ##############################