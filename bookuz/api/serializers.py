from rest_framework import serializers
from .models import Book, Author, Category, Comment, Carousel


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'book', 'text']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    book_author = AuthorSerializer(read_only=True)
    book_author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='book_author', write_only=True)
    book_category = CategorySerializer(read_only=True)
    book_category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='book_category', write_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'book_name', 'book_author', 'book_author_id', 'book_category',
            'book_category_id', 'book_price', 'book_year', 'book_language',
            'book_description', 'book_pages_count', 'book_rating', 'book_publisher',
            'book_cover', 'book_photos', 'comments'
        ]

class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = '__all__'
