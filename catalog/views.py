from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from taggit.models import Tag
from .models import Movie
from .forms import ReviewForm

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
    
    # override the context data to pass similar movies
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   # run the parent method to get the movie object
        # get movies which have most tags in common
        context['similar_movies_list'] = None
        movie = self.get_object()
        genres_id_list = movie.genres.values_list('id', flat=True)
        similar_movies_list = Movie.objects.filter(genres__in = genres_id_list).exclude(id=movie.id)
        similar_movies_list = similar_movies_list.annotate(similar_movies=Count('genres')).order_by('-similar_movies', 'release_date')[:4]
        
        context['similar_movies_list'] = similar_movies_list
        context['form'] = ReviewForm()
        
        return context
    

@require_POST
def review_post(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    review = None
    current_user = None
    
    if request.user.is_authenticated:
        current_user = request.user
        
    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.movie = movie
        review.author = current_user
        review.save()

        return redirect(movie.get_absolute_url())
    
    return render(request, 'catalog/movie/review.html', {'form': form, 'movie': movie, 'review': review})