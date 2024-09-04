from django.db.models.signals import post_save
from django.core.signals import request_started, request_finished
from django.dispatch import receiver
from .models import Review

@receiver(post_save, sender=Review, dispatch_uid="my unique id")
def new_movie_alert(sender, instance, created, **kwargs):
    if created:
        print("New Review added", instance.movie)
        
    else:
        print('I am changed')
        
        
@receiver(request_started, dispatch_uid="unique_request_id")
def request_alert(sender, environ, **kwargs):
    print("---------------------------Request Started-----------------------")
    
    
@receiver(request_finished, dispatch_uid="unique_request_end_id")
def request_end_alert(sender, **kwargs):
    print("---------------------------Request Ended------------------------")