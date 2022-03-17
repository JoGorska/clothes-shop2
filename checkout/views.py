import os
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from django.conf import settings
from .forms import OrderForm
from bag.contexts import bag_contents

import stripe


def checkout(request):
    '''
    view to make checkout
    '''
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    # stripe requires the payment to be passed as integer
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
        automatic_payment_methods={
            'enabled': True,
        },
    )
    print(f'THIS IS INTENT {intent.payment_method_options}')
    # print(f'THIIS IS PAYMENT_METHOD {intent.payment_method}')
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your enviroment?')
    order_form = OrderForm()
    template = 'checkout/checkout.html'

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)
