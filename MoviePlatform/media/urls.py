from django.urls import path

from media import views

urlpatterns = [
    path('genres/', views.GenreViewSet.as_view, name='genres'),
    path('countries/', views.CountryViewSet.as_view, name='countries'),
    path('movies/', views.MovieViewSet.as_view, name='movies'),
    path('tvshows/', views.TVShowViewSet.as_view, name='tvshows'),
    path('ratings/', views.RatingViewSet.as_view, name='ratings'),
]
