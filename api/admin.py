from django.contrib import admin
from .models import Book, Author, Category, Carousel, OTP, UserProfile, OrderItem, Order

admin.site.register(Book)
# admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Carousel)
admin.site.register(OTP)
admin.site.register(UserProfile)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
