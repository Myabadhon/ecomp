from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from twilio.rest import Client
import datetime
import json


# Create your views here.


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action :', action)
    print('productId :', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = orderItem.quantity+1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity-1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('It was added...', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                country=data['shipping']['country'],
                city=data['shipping']['city'],
                district=data['shipping']['district'],
                subdistrict=data['shipping']['subdistrict'],
                postalcode=data['shipping']['postalcode'],
            )
        sid = "AC2c1a77273403f41ede9e00a43bee36c7"
        authToken = "5a53dc6fba3ddd9428ba3eafe9545a83"
        client = Client(sid, authToken)
        sender_number = "whatsapp:+14155238886"
        receiver_number = "whatsapp:+8801953636469"
        #Order No: 00000 , Product url: ,Your payment {}
        message = "Hello {},Your payment {}has been successfully completed".format(customer, total)
        client.messages.create(to=receiver_number, from_=sender_number, body=message)
        print("Whatsapp Notification Done")
    else:
        print("User not logged in ..")

    return JsonResponse('Payment Completed...', safe=False)

