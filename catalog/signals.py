from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review

@receiver(post_save, sender=Review, dispatch_uid="my unique id")
def new_movie_alert(sender, instance, created, **kwargs):
    if created:
        print("New Review added", instance.movie)
        
    else:
        print('I am changed')
    