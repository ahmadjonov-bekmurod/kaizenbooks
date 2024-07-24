from django_filters import rest_framework as filters
from .models import Book


class BookFilter(filters.FilterSet):
    book_name = filters.CharFilter(lookup_expr='icontains')
    book_author = filters.CharFilter(field_name='book_author__name', lookup_expr='icontains')
    book_category = filters.CharFilter(field_name='book_category__name', lookup_expr='icontains')
    book_year = filters.NumberFilter()
    book_language = filters.CharFilter(lookup_expr='icontains')
    book_price = filters.NumberFilter()

    class Meta:
        model = Book
        fields = [
            'book_name', 'book_author', 'book_category', 'book_year',
            'book_language', 'book_price'
        ]
