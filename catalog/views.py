from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Movie

# Create your views here.

class MovieListView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = 'catalog/movie/list.html'

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'catalog/movie/detail.html'
    context_object_name = 'movie'
    
    def get_object(self):
        return get_object_or_404(
            Movie,
            slug=self.kwargs['movie'],
            release_date__year=self.kwargs['year'],
            release_date__month=self.kwargs['month'],
            release_date__day=self.kwargs['day'],
        )