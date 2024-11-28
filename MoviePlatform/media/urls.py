from django.urls import path

from media import views

urlpatterns = [
    path('', views.MediaView.as_view(), name='media'),
    path('movie/<int:pk>/', views.MovieView.as_view(), name='movie'),
]