from django.db import models
from django.contrib.auth.models import User
import random


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
    book_price = models.IntegerField(default=0)
    book_year = models.IntegerField(default=0)
    book_language = models.CharField(max_length=50, blank=True)
    book_description = models.TextField(blank=True)
    book_pages_count = models.IntegerField(default=0)
    book_rating = models.FloatField(default=0)
    book_publisher = models.CharField(max_length=255, default=None)
    book_cover = models.ImageField(upload_to='covers/', blank=True, null=True)

    # book_photos = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return self.book_name


class Comment(models.Model):
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:20]


class Carousel(models.Model):
    image_en = models.ImageField(upload_to='carousel_images/en/', blank=True, null=True)
    image_ru = models.ImageField(upload_to='carousel_images/ru/', blank=True, null=True)
    image_uz = models.ImageField(upload_to='carousel_images/uz/', blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    description_uz = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Carousel Item {self.id}'


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    delivery_method = models.CharField(max_length=100)
    address = models.TextField()
    payment_method = models.CharField(max_length=100)
    promo_code = models.CharField(max_length=50, blank=True, null=True)
    order_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.book.book_name}"


def generate_otp():
    return ''.join(random.choices('0123456789', k=6))


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, default=generate_otp)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} Profile"