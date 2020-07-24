from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import Usersignup
from django.core.mail import send_mail, EmailMultiAlternatives
from whatsbussy.settings import MYEMAIL, MYPASSWORD
import json
from django.template.loader import render_to_string, get_template
import re
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Product, subscription, UsersDetails
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from whatsbussy.settings import STRIPEAPI
# Create your views here.

users_dicts = {}
email_pattern = re.compile(
    r'^([_\-\.a-zA-Z0-9]+)@([_\-\.a-zA-Z]+)\.([a-zA-Z]){2,7}$')
namepattern = re.compile(r'[a-zA-Z]+')
userpattern = re.compile(r'[a-zA-Z0-9\.\-_@]+')
passpattern = re.compile(r'[a-zA-Z0-9\.-_@]{8,}')
phonepattern = re.compile(r'[0-9]{10}')
zipcodepattern = re.compile(r'[0-9]{6}')

choices = (
    (1, 'Active'),
    (2, 'trail'),
    (3, 'trai_end'),
    (4, 'past_due'),
    (5, 'unpaid'),
    (6, 'cancel'),
    (7, 'incomplete'),
    (8, 'incomplete_expired')
)

stripe.api_key = STRIPEAPI


def give_status(status):
    for i in choices:
        if i[1] == status:
            return i[0]
    return 0

# Home Page of Our Web Application


def home(request):
    context = {}
    if request.user.is_authenticated:
        basic = Product.objects.filter(pid='prod_Hgh9YBYSJVdToh').first()
        premium = Product.objects.filter(pid='prod_HggtcEDwyez0mH').first()
        basicsub = subscription.objects.filter(
            user=request.user, product=basic).first()
        premsubs = subscription.objects.filter(
            user=request.user, product=premium).first()
        if basicsub != None:
            context['hasbasic'] = 1
        if premsubs != None:
            context['haspremium'] = 1
    return render(request, 'subcriptions/home.html', context=context)

# OUR User SIGNUP View


def SIGNUP(request):
    context = {}
    context['form'] = Usersignup()
    return render(request, 'subcriptions/signup.html', context=context)

# This View will handle Logic for Signup,because form at signup page will be submitted Asynchronously Using Ajax.


def signup(request):
    data = {}
    if request.method == 'POST':
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']

        fname = firstname.replace(' ', '').isalpha()  # validating name
        lname = lastname.replace(' ', '').isalpha()  # validating  lastname

        obj = User.objects.all()
        found = 0
        for i in obj:  # cheking is there any user with give email id
            if i.email == email:
                found = 1  # if we found user , then assign 1 to found and break from the loop
                break

        if fname == True and lname == True and found == 0:
            customer = stripe.Customer.create(  # regestring this user in  stripe , we will need this later.
                email=email
            )

            obj = User.objects.create_user(
                email.split('@')[0], email, password)  # Creating Object of user in Our Database
            obj.first_name = firstname
            obj.last_name = lastname
            obj.save()

            user_Details = UsersDetails(
                cust_id=customer['id'], user=obj)  # customer is an object which is return by stripe , we just store it in our database
            user_Details.save()

            # User Successfully Created , sending to client side
            data = {'created': 1}

            return HttpResponse(json.dumps(data),  content_type="application/json")
        if fname == False:
            data['notvalidname'] = 'true'
        if lname == False:
            data['notvalidlastname'] = 'true'
        if found == 1:
            data['userexists'] = 'true'

        return HttpResponse(json.dumps(data),  content_type="application/json")

# Login Page for users


def Login(request):
    return render(request, 'subcriptions/login.html')


# This View handles the authentication , User are Redirect to their Account if they are Authenticated
def logins(request):
    # print('came')
    data = {}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if '@' in email:  # validating email
            user = User.objects.filter(email=email).first()
        else:
            data = {'nouser': 'Please enter valid Email Address'}
            return HttpResponse(json.dumps(data),  content_type="application/json")

        if user is not None:  # if user with email is present then we will check password , if thery are matching,then we will log the user in.
            if check_password(password, user.password) == True:
                login(request, user)
                data = {'valid': 1}
            else:
                data = {
                    'wrongpassword': 1
                }
            return HttpResponse(json.dumps(data), content_type="application/json")

        # if passwords are not matching we will tell the user , please provide a correct password.
        if (user is not None) and (user.password != password):
            data = {
                'wrongpassword': 1
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {
                'nouser': 'Please enter valid Email Address'
            }
        return HttpResponse(json.dumps(data),  content_type="application/json")


# Page  for Premium Package Subscription
@login_required(login_url='Login')
def subscriptionofPremiunm(request):
    context = {}
    return render(request, 'subcriptions/subscriptionofPremiunm.html', context=context)


# Actual page where , User can Access the Premium Product if he has subscription for Premium Package
@login_required(login_url='Login')
def Premiunm(request):
    context = {}
    # fetching details for premium package
    prduct = Product.objects.filter(pid="prod_HggtcEDwyez0mH").first()
    sub = subscription.objects.filter(
        user=request.user, product=prduct).first()  # checking whether user has subscription  for premiun Products.

    if sub != None:  # if user has subscription  for premiun Products, we will navigate to page where user can access premium products
        return render(request, 'subcriptions/Premiunm.html', context=context)
    else:  # otherwise we will dispplay access denied message to user
        return HttpResponse('<h1>Ypu Dont have Permission to access this content</h1>')


# handles process for Premium subscription.
def makesubscription(request):
    if request.method == 'POST':
        holdername = request.POST['name']
        cardNumber = request.POST['cardNumber']
        cardType = request.POST['cardType']
        name = request.POST['name']
        # Collecting credict cards details from user
        expiryMonth = request.POST['expiryMonth']
        expiryYear = request.POST['expiryYear']
        cvc = request.POST['cvc']
        subtype = request.POST['subtype']

        userdetails = UsersDetails.objects.filter(
            user=request.user).first()  # fetching user details from database

        payment = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": cardNumber,  # Creating payment method for user
                "exp_month": int(expiryMonth),
                "exp_year": int(expiryYear),
                "cvc": cvc,
            },
        )
        # print(payment)

        stripe.PaymentMethod.attach(
            payment['id'],
            # WE will attach created payment method for this user as payment method.
            customer=userdetails.cust_id,
        )

        # Set the default payment method on the customer
        stripe.Customer.modify(
            userdetails.cust_id,  # cust_id is giving from stripe, recall in signup view we  have created customer for stripe, so it is required here
            invoice_settings={
                'default_payment_method': payment['id'],
            },
        )

        # Not for NOW But for future we will handle every subscription ,from this same view.So we are checking whether request is for premium or for other package
        if subtype == 'Premium':
            # subscription in stripe
            subscriptionstripe = stripe.Subscription.create(
                # creating subscription for by providing user stripe id mean customer id for stripe.
                customer=userdetails.cust_id,
                # preice id is nothing but just id given by stripe for premium products
                items=[{"price": "price_1H6f9EEoanPy9ym0tdMzwzKh"}],
                # As premuim package contain free 7 days trail so we are passing trail_period _parameter
                trial_period_days=7,
            )

            package = Product.objects.filter(
                pid="prod_HggtcEDwyez0mH").first()

            # now we will collect the subscription details from stripe subscription object "subscriptionstripe" and store in our database so that we can validate the users.
            subs = subscription(
                sub_id=subscriptionstripe['id'], product=package, user=request.user)
            subs.save()

            messages.success(
                request, 'Your Subscription for Premium Pakage iS done Successfully and currently it is in trail state.')
        else:
            # Subscription for basic Package
            subscriptionstripe = stripe.Subscription.create(
                customer=userdetails.cust_id,
                items=[{"price": "price_1H6f9EEoanPy9ym0tdMzwzKh"}],
            )

            package = Product.objects.filter(
                pid="prod_HggtcEDwyez0mH").first()  # pid is id for basic package product given by stripe.
            subs = subscription(
                sub_id=subscriptionstripe['id'], product=package, user=request.user)
            subs.save()

            messages.success(
                request, 'Your Subscription for Basic Pakage iS done Successfully and currently it is in Active state.')
        data = {'success': 1}
        return HttpResponse(json.dumps(data),  content_type="application/json")


# Page where user can access basic package product
@login_required(login_url='Login')
def Basic(request):
    context = {}
    prduct = Product.objects.filter(pid="prod_Hgh9YBYSJVdToh").first()

    sub = subscription.objects.filter(
        user=request.user, product=prduct).first()  # checking whether userr has subscription  for basic products or not

    if sub != None:
        return render(request, 'subcriptions/basic.html', context=context)
    else:
        return HttpResponse('<h1>Ypu Dont have Permission to access this content</h1>')

# view where user can take subscription for basic package


@login_required(login_url='Login')
def makebasicsubscription(request):
    context = {}

    # Priceid for basic pacakge products
    PRICE_ID = "price_1H7JlYEoanPy9ym0axqMesQx"

    customer = UsersDetails.objects.filter(
        user=request.user).first()  # fetching details from our datbase

    session = stripe.checkout.Session.create(  # building seesion
        payment_method_types=['card'],
        line_items=[{
            'price': PRICE_ID,
            'quantity': 1,
        }],
        mode='subscription',
        # if subscription is done successfully then user is redirected to this url
        success_url='http://localhost:8000/success/session_id={CHECKOUT_SESSION_ID}/',
        # Otherwise user will redirect to this url
        cancel_url='http://localhost:8000/cancel/',
        customer=customer.cust_id
    )
    context['seesionid'] = session['id']
    return render(request, 'subcriptions/makebasicsub.html', context=context)


# success view for basic package subscription

@login_required(login_url='Login')
def success(request, CHECKOUT_SESSION_ID):
    messages.success(
        request, 'Your Subscription for Basic package has been done  Successfully for the next 30 days.So , enjoy and stay tuned for the latest offers and updates.')
    return redirect('Basic')


# cancel view for basic package subscription

@login_required(login_url='Login')
def cancel(request):
    messages.success(
        request, 'Your Subscription process was failed.')
    return redirect('home')


# important view  , which is know as webhook where stripe  sends various notification to this endpoint
# this decoator will allow stripe to make post request to this view.
@csrf_exempt
def subscription_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    print(f'{event.type} = {event.data.object}')
    # handling customer.subscription.trial_will_end end event
    if event.type == 'customer.subscription.trial_will_end':
        subscriptions = event.data.object
        print(subscriptions)

    elif event.type == 'invoice.created':
        subscriptionend = event.data.object  # contains a stripe.invoice
        print(subscriptionend, 'here')

        # obj = subscription.objects.filter(
        #     sub_id=subscriptionend.customer).first()
        # obj.sub_status = 3
        # obj.save()
        product = Product.objects.filter(
            pid=subscriptionend.lines.data[0].price.product).first()

        customer = UsersDetails.objects.filter(
            cust_id=subscriptionend.customer).first()

        obj = subscription.objects.filter(
            product=product, user=customer.user).first()

        if obj != None:
            subs_Status = stripe.Subscription.retrieve(obj.sub_id).status
            print(subs_Status, 'status')
        else:
            print('No subscription found')
        return HttpResponse('<h1> response is successful</h1>')

    # one of the important event customer subscriptions updation event
    elif event.type == 'customer.subscription.updated':
        obj = event.data.object
        subs_status = obj.status
        subs = subscription.objects.filter(sub_id=obj.id).first()

        # if subs is not present in our database then we will create an new subscription in our database from receive data from the event
        if subs == None:
            product = Product.objects.filter(
                pid=obj.items.data[0].plan.product).first()

            subs = subscription(sub_id=obj.id, product=product, user=request.user, sub_status=give_status(obj.status), created_at=datetime.fromtimestamp(
                obj.created), current_start_at=datetime.fromtimestamp(obj.current_period_start), current_end_at=datetime.fromtimestamp(obj.current_period_end))
            subs.save()

        else:
            # saving the current status of subscription in our Database

            # we  got subs_status from stripe which is a string but we have store status as a number,
            # so for that we will pass that string to funcion and that will return coressponding integer value
            subs.sub_status = give_status(subs_status)
            subs.save()

            # if after updation subscription is active we will update information in database as well to track user.
            if obj.status == 'active':
                endtimestamp = obj.current_period_end
                starttimestamp = obj.current_period_start
                # changing current period end for the subscrption
                subs.current_end_At = datetime.fromtimestamp(endtimestamp)
                subs.current_start_at = datetime.fromtimestamp(starttimestamp)
                subs.sub_status = give_status(subs_status)
                subs.save()
                print(
                    f'our data {endtimestamp} {starttimestamp} {subs} {subs_status} {obj} are dataa')
            elif obj.status == 'past_due':
                pass
            elif obj.status == 'unpaid':
                pass
            elif obj.status == 'canceled':
                pass
            elif obj.status == 'incomplete':
                pass
            elif obj.status == 'incomplete_expired':
                pass
            elif obj.status == 'trailing':
                pass
            else:
                pass

    elif event.type == 'invoice.payment_succeeded':  # handling invoice payment succeeded event
        obj = event.data.object
        endtimestamp = obj.lines.data[0].period.end
        starttimestamp = obj.lines.data[0].period.start
        subs = obj.lines.data[0].subscription
        subsobject = stripe.Subscription.retrieve(subs)
        print(subsobject)
        customer = obj.customer

    else:
        # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)


# page where user can manage there subscriptions for various products
@login_required(login_url='Login')
def MySubscription(request):
    context = {}
    obj = subscription.objects.filter(~Q(sub_status=5))
    context['subscription'] = obj
    return render(request, 'subcriptions/mysubscription.html', context=context)

# view which handles  preocess of cancellation of subscription.


def cancel_mysubscription(request):
    if request.method == 'POST':
        sub_id = request.POST['sub_id']

        stripe.Subscription.delete(sub_id)  # subscription cancellation

        subs = subscription.objects.filter(
            sub_id=sub_id).first()  # update user  subscription in our database.
        subs.sub_status = 5  # 5 is integer value for canceled status
        subs.save()

        messages.success(
            request, f'Your Subscription for {subs.product.pname} has been canceled.')
        data = {'success': 1}
        return HttpResponse(json.dumps(data),  content_type="application/json")

# Logout view


def LOGOUT(request):
    logout(request)
    return redirect('home')
