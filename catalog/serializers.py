from rest_framework import serializers
from .models import Language, Country, Movie, Review, Person
from taggit.models import Tag

class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ['url', 'id','title']
        
class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ['url', 'id', 'name']
        
class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ['url', 'id', 'name', 'role']
        
        
class MovieSerializer(serializers.HyperlinkedModelSerializer):
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all()) 
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    actors = serializers.PrimaryKeyRelatedField(many=True, queryset = Person.objects.all().filter(role=Person.PersonRoles.ACTOR))
    director = serializers.PrimaryKeyRelatedField(queryset = Person.objects.all().filter(role=Person.PersonRoles.DIRECTOR))
    genres = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    reviews = serializers.HyperlinkedRelatedField(many=True, view_name='review-detail', read_only=True)
    class Meta:
        model = Movie
        fields = ['url', 'id', 'title', 'poster', 'release_date', 'slug', 'plot', 'imdb_rating', 
                  'duration' , 'movie_duration', 'average_rating', 'language', 'genres', 'director', 
                  'actors', 'country', 'reviews' ,'created', 'updated' ]
        
        
        
class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Review
        fields = ['url', 'title', 'body', 'rating', 'author', 'movie', 'created', 'updated']
        
        
class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        
    