from django.shortcuts import render
from django.views.generic import ListView
from .models import Movie

# Create your views here.

class MovieListView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = 'catalog/movie/list.html'

