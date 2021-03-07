from django.shortcuts import render , redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder

from .forms import CreateUserForm

from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required ,permission_required

from .decorators import unauthenticated_user , paied_users

#sign in view
@unauthenticated_user
def signin(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid() :
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            users = User.objects.all()
            customer = Customer( user=users[len(users)-1] ,name = username , email =email)
            customer.save()
            messages.success(request , "Account was created for " + username)
            return redirect('login')

    context = {'form' : form}
    return render(request , 'accounts/signin.html' , context)


#sign in view
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request , username=username , password=password)
        if user is not None :
            login(request , user)
            return redirect('store')
        else :
            messages.info(request , "Username Or Password is incorrect")

    context = {}
    return render(request , 'accounts/login.html' , context)


def logOutUser(request):
    logout(request)
    return redirect('store')

@login_required(login_url="login")
@paied_users(allowed_roles = ['admin' , 'paied_users'])
def addPost(request):
    return render(request , 'store/addpost.html')

@login_required(login_url="login")
def paytopost(request):
    return render(request , 'store/paytopost.html')

@login_required(login_url="login")
def pay(request):
    user = request.user
    user.groups.clear()
    user.groups.add(2)
    return redirect ('addpost')

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

#change update item logic
@login_required(login_url="login")
@paied_users(allowed_roles = ['admin' , 'paied_users'])
def updateItem(request , pk):
	pass

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)