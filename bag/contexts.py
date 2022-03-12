from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    '''
     context processor, make this dictionary available to all templates across
     the entire application
    '''
    # bag_items is a list of dictionaries from a for loop below
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    # forloops all items in the bag gets the product, quantity and price
    # appends the list bag_items with the dictionary of item id, quantity and product name
    for item_id, quantity in bag.items():
    
        product = get_object_or_404(Product, pk=item_id)
        total += int(quantity) * product.price
        product_count += int(quantity)
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
