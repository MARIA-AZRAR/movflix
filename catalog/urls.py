from django.urls import path
from .views import MovieListView

app_name = 'catalog'

urlpatterns = [
    path('', MovieListView.as_view(), name='movies'), 
    # path('detail/<int:id>/'),
]