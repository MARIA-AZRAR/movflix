from django.urls import include, path
from .views import FeedbackFormView, MovieListView, MovieDetailView, MovieViewSet, ReviewViewSet, SuccessView, \
review_post, LanguageViewSet, CountryViewSet, TagViewSet, PersonDetailView, PersonListView
from rest_framework.routers import DefaultRouter


# app_name = 'catalog'

router = DefaultRouter()
router.register(r'languages', viewset=LanguageViewSet, basename='language')
router.register(r'countries', viewset=CountryViewSet, basename='country')
# router.register(r'persons', viewset=PersonViewSet, basename='person')
router.register(r'movies', viewset=MovieViewSet, basename='movie')
router.register(r'reviews', viewset=ReviewViewSet, basename='review')
router.register(r'tags', viewset=TagViewSet, basename='tag')
 
urlpatterns = [
    path('', include(router.urls)),
    path('persons', PersonListView.as_view(), name='person-list'),
    path('persons/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path("email/", FeedbackFormView.as_view(), name="feedback"),
    path("success/", SuccessView.as_view(), name="success"),
    # path('', MovieListView.as_view(), name='movies'), 
    # path('<slug:genre_slug>/', MovieListView.as_view(), name='movie_list_by_genre'),
    # path('<slug:movie>/<int:year>/<int:month>/<int:day>/', MovieDetailView.as_view(), name='movie_detail'),
    # path('<int:movie_id>/review/', review_post, name='post_review'),
]