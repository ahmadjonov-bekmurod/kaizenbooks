from django.contrib import admin
from .models import Book, Comment, Author, Category, Carousel, OTP, Order, UserProfile

admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Carousel)
admin.site.register(OTP)
admin.site.register(Order)
admin.site.register(UserProfile)
