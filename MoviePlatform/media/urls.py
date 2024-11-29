from django.urls import path

from media import views

urlpatterns = [
    path('', views.MediaView.as_view(), name='media'),
    path('movie/<int:pk>/', views.MovieView.as_view(), name='movie'),
    path('tvshow/<int:pk>/', views.TVShowView.as_view(), name='tvshow'),
    path('add_movie/', views.AddMovieView.as_view(), name='add_movie'),
    path('add_tvshow/', views.AddTVShowView.as_view(), name='add_tvshow'),
]