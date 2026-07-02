from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import *

@receiver(post_save, sender=Booking)
def clear_cache_on_post(sender, instance, **kwargs):
    cache.delete(f'booking_{instance.pk}')
    
@receiver(post_delete, sender=Booking)
def clear_cache_on_delete(sender, instance, **kwargs):
    cache.delete(f'booking_{instance.pk}')
