from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User

@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = instance.telegram_id
