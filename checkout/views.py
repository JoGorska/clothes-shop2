import os
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

if os.path.isfile("env.py"):
    import env
from django.conf import settings
from .forms import OrderForm
from bag.contexts import bag_contents

import stripe


def checkout(request):
    '''
    view to make checkout
    '''
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    # stripe requires the payment to be passed as integer
    stripe_total = round(total * 100)
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    stripe_public_key = os.environ.get('stripe_public_key')
    client_secret = os.environ.get('client_secret')
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': client_secret,
    }
    return render(request, template, context)
