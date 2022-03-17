from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product

# Create your views here.


def view_bag(request):
    """
    A view that renders a bag content page
    """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    Add quantity of the specified product to the shopping bag
    """
    product = get_object_or_404(Product, pk=item_id)
    # it will come from template as a string - need to convert to integer
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})
    # if item has a size it checks if item of that size already in the bag
    # increments the number of items with this size
    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} qantity to {bag[item_id]["items_by_size"][size]}')
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    # if no size - increments the quantity of items
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of products in the shopping bag
    to the specified amount
    """
    product = get_object_or_404(Product, pk=item_id)
    # it will come from template as a string - need to convert to integer
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})
    # if item has a size it checks if item of that size already in the bag
    # increments the number of items with this size
    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} qantity in {bag[item_id]["items_by_size"][size]}')
        else:
            # if the quantity is set to zero 
            del bag[item_id]['items_by_size'][size]
            # if zero items of particular size, remove item from bag
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
                messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
    # if no size - increments the quantity of items
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    Remove item from the shopping bag
    """
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})
        # if item has a size it checks if item of that size already in the bag
        # increments the number of items with this size
        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')

    # if no size - increments the quantity of items
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')
        request.session['bag'] = bag
        # instead of redirecting, we want return status 200
        # implying that item was successfully removed
        # this view will be posted to from javascript function
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
