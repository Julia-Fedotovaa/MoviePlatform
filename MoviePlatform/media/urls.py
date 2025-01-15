"""Модуль, отвечающий за маршрутизацию приложения media."""
from django.urls import path

from media import views

urlpatterns = [
    path('', views.MediaView.as_view(), name='media'),
    path('movie/<int:pk>/', views.MovieView.as_view(), name='movie'),
    path('tvshow/<int:pk>/', views.TVShowView.as_view(), name='tvshow'),
    path('add_movie/', views.AddMovieView.as_view(), name='add_movie'),
    path('add_tvshow/', views.AddTVShowView.as_view(), name='add_tvshow'),
    path('complex_querries/', views.ComplexQueriesView.as_view(), name='complex_querries'),
    path('media/', views.media_list_view, name='media_list'),
    path('media/<int:pk>/', views.media_detail_view, name='media_detail'),
    path('media/<int:pk>/rate/<int:rating>/edit/', views.ReviewEditView.as_view(), name='rate_media'),
    path('media/<int:pk>/rate/<int:rating>/delete/', views.ReviewDeleteView.as_view(), name='delete_rating'),
    path('add_media/', views.add_media_view, name='add_media'),
]
