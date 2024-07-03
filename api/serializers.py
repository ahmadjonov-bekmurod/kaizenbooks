from rest_framework import serializers
from .models import Book, Author, Category, Comment, Carousel, OrderItem, Order
from django.contrib.auth.models import User
from .models import OTP


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
            'book_cover', 'comments'
        ]


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            book_data = item_data.pop('book')
            book = Book.objects.get(id=book_data['id'])
            OrderItem.objects.create(order=order, book=book, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.delivery_method = validated_data.get('delivery_method', instance.delivery_method)
        instance.address = validated_data.get('address', instance.address)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.promo_code = validated_data.get('promo_code', instance.promo_code)
        instance.order_comment = validated_data.get('order_comment', instance.order_comment)
        instance.save()

        for item_data in items_data:
            book_data = item_data.pop('book')
            book = Book.objects.get(id=book_data['id'])
            order_item, created = OrderItem.objects.update_or_create(order=instance, book=book, defaults=item_data)
        return instance


from rest_framework import serializers
from .models import OTP

class OTPCreateSerializer(serializers.ModelSerializer):
    user_phone_number = serializers.CharField(source='user.userprofile.phone_number', read_only=True)

    class Meta:
        model = OTP
        fields = ['user_phone_number', 'otp']

from rest_framework import serializers
from .models import OTP

class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')
        try:
            user = User.objects.get(userprofile__phone_number=phone_number)
            otp_instance = OTP.objects.get(user=user, otp=otp, is_verified=False)
        except (User.DoesNotExist, OTP.DoesNotExist):
            raise serializers.ValidationError("Invalid OTP or Phone Number")
        return data


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['password', 'first_name', 'last_name', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract profile related fields from validated_data
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        phone_number = validated_data.pop('phone_number')

        # Generate a unique username (you can customize this logic if needed)
        username = f"user_{User.objects.count() + 1}"

        # Create the User object
        user = User.objects.create_user(username=username, **validated_data)

        # Create the UserProfile object
        UserProfile.objects.create(user=user, first_name=first_name, last_name=last_name, phone_number=phone_number)

        return user
