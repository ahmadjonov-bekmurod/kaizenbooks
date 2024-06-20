from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    book_name = models.CharField(max_length=255, default=None, null=False, blank=False)
    book_author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE, null=True)
    book_category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE, default=None)
    book_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    book_year = models.IntegerField(default=0)
    book_language = models.CharField(max_length=50, blank=True)
    book_description = models.TextField(blank=True)
    book_pages_count = models.IntegerField(default=0)
    book_rating = models.FloatField(default=0)
    book_publisher = models.CharField(max_length=255, default=None)
    book_cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    book_photos = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return self.book_name


class Comment(models.Model):
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:20]
