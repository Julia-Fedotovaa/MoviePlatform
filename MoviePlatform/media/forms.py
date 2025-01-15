from django import forms
from .models import Media


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'release_date', 'country', 'genres', 'type', 'poster', 'rating', 'file', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genres': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'poster': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название',
            'release_date': 'Дата выпуска',
            'genres': 'Жанры',
            'type': 'Тип',
            'poster': 'Постер',
            'rating': 'Рейтинг',
            'file': 'Файл',
            'url': 'Ссылка',
        }
        help_texts = {
            'rating': 'Оценка от 0 до 10.',
        }
        error_messages = {
            'title': {
                'max_length': 'Название не может превышать 255 символов.',
            },
        }
