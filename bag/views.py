from django.shortcuts import render, redirect

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
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    # if no size - increments the quantity of items
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)
