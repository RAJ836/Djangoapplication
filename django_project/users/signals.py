#post_save is a signal which is triggered after when an object is saved
from django.db.models.signals import post_save
from django.contrib.auth.models import User
#reciever is a fucntion which recieves the signal
from django.dispatch import receiver
from .models import Profile


"""
    when an user is saved a signal ('post_save') is triggered , then the receiver receives the signal
    and then it is routed to 'create_profile 'function creates a profile for that user.
"""
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        # profile=Profile(user=instance)
        # profile.save()
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()