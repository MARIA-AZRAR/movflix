from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from taggit.models import Tag
from .models import Movie

# Create your views here.

class MovieListView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = 'catalog/movie/list.html'
    paginate_by = 8
    
    # override queryset to pass the movies with the slug only
    def get_queryset(self):
        queryset = Movie.objects.all()
        genre_slug = self.kwargs.get('genre_slug')
        
        if genre_slug:
            genre = get_object_or_404(Tag, slug=genre_slug)
            queryset = queryset.filter(genres__in = [genre])
        
        return queryset
    
    # override the context data to pass genre slug to the template as well
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   # run the parent method to get the movies object
        genre_slug = self.kwargs.get('genre_slug')
        context['genre'] = None
        if genre_slug:
            context['genre'] = get_object_or_404(Tag, slug=genre_slug)
        return context
            
        

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