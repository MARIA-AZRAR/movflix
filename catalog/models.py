from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg

from taggit.managers import TaggableManager

# Create your models here.

class Language(models.Model):
    title = models.CharField(max_length=100, null=False)
    
    def __str__(self):
        return self.title
    
class Country(models.Model):
    name = models.CharField(max_length=100, null=False)
    
    def __str__(self):
        return self.name

class Person(models.Model):
    class PersonRoles(models.TextChoices):
        ACTOR = 'AC', 'Actor'
        DIRECTOR = 'DC', 'Director'
        
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=10, choices=PersonRoles.choices)
    
    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=250)
    poster = models.CharField(max_length=250)
    release_date = models.DateField()
    slug = models.SlugField(max_length=250, unique_for_date='release_date')
    plot = models.TextField()
    imdb_rating = models.IntegerField()
    duration = models.DurationField()
    
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='lang_movies')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_movies')
    actors = models.ManyToManyField(Person, related_name='acted_in', limit_choices_to={'role': Person.PersonRoles.ACTOR})
    director = models.ForeignKey(Person, related_name='directed', on_delete=models.CASCADE, limit_choices_to={'role': Person.PersonRoles.DIRECTOR})
    
    genres = TaggableManager()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-release_date']
        
        indexes = [
            models.Index(fields=['-release_date']),
        ]
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('catalog:movie_detail', args=[self.slug, self.release_date.year, self.release_date.month, self.release_date.day])
        
    @property
    def movie_duration(self):
        """
        format the movie duration
        :return string:
        """
        total_minutes = int(self.duration.total_seconds() // 60)  # convert timedelta to total minutes, ensuring it's an integer
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours} hr {minutes} min" if hours else f"{minutes} min"

    @property
    def average_rating(self):
        """
        return average user rating for a movie
        :return float:
        """
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return avg_rating or 0

class Review(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        
    def __str__(self):
        return f'Review by {self.author.username} on {self.movie}'
    
    
     