from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from chatrooms.models import Chat, Msg


@receiver(post_save, sender=User)
def create_user_room(sender, instance, created, **kwargs):
    if created:
        json = {
            'name': instance.username,
            'slug': instance.username,
            'owner': instance.username,
        }
        Chat.objects.create(**json)