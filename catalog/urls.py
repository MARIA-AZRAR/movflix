from django.urls import path
from .views import MovieListView, MovieDetailView

app_name = 'catalog'

urlpatterns = [
    path('', MovieListView.as_view(), name='movies'), 
    path('<slug:genre_slug>/', MovieListView.as_view(), name='movie_list_by_genre'),
    path('<slug:movie>/<int:year>/<int:month>/<int:day>/', MovieDetailView.as_view(), name='movie_detail'),
]