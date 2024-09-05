from django.core.management.base import BaseCommand, CommandError, no_translations
from catalog.models import Movie

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('movie_ids', nargs='+' ,type=int)
    
        parser.add_argument('--delete', action='store_true', help='delete the movie')
        
    @no_translations # this is for not bothering and saving translated content
    def handle(self, *args, **options):
        for movie_id in options['movie_ids']:
            try:
                movie = Movie.objects.get(id=movie_id)
            except Movie.DoesNotExist:
                raise CommandError('Movie "%s" does not exist' % movie_id)
            
            if options['delete']:
                movie.delete()
                
                self.stdout.write(
                    self.style.SUCCESS('Successfully deleted the movie "%s"' % movie.title)
                )
            else:  
                movie.award = True
                movie.save()
            
                self.stdout.write(
                    self.style.SUCCESS('Successfully gave award to "%s"' % movie.title)
                )
                
