from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem())
def update_on_save(sender, instance, created, **kwards):
    """
    handles signals from post save event
    sender of the signal - update/ create order line item
    instance of the model - sends it
    created - boleon if this is a new instance or update
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem())
def update_on_delete(sender, instance, **kwards):
    """
    signal for deleting the item
    """
    instance.order.update_total()
