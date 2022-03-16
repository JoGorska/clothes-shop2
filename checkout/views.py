from django.shortcuts import render, redirect, reverse
from django.contrib import messages
import os
if os.path.isfile("env.py"):
    import env

from .forms import OrderForm

def checkout(request):
    '''
    view to make checkout
    '''
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
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
