from django.contrib import admin
from .models import Movie, Review, Language, Country, Person
# Register your models here.

admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Person)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'imdb_rating', 'release_date']
    list_filter = ['release_date', 'title', 'imdb_rating']
    search_fields = ['title', 'plot']
    prepopulated_fields = {'slug': ('title',)}
    
    date_hierarchy = 'release_date'
    ordering = ['release_date', 'imdb_rating']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
 list_display = ['title', 'rating', 'movie', 'created', 'author']
 list_filter = ['rating', 'created', 'updated']
 search_fields = ['title', 'body']