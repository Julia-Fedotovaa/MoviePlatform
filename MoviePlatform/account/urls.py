from django.urls import path, include
from .views import AccountView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('account/', AccountView.as_view(), name='account'),
    path('', include('django.contrib.auth.urls')),  # Встроенные маршруты
    # Другие маршруты
]
