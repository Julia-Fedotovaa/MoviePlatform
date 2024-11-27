from django.urls import path
from rest_framework import routers

from media import views

router = routers.DefaultRouter()
router.register(r'genres', views.GenreViewSet)
router.register(r'countries', views.CountryViewSet)
router.register(r'movies', views.MovieViewSet)
router.register(r'tvshows', views.TVShowViewSet)
router.register(r'ratings', views.RatingViewSet)
router.register(r'complex-query', views.ComplexQueryView, basename='complex-query')

urlpatterns = router.urls
