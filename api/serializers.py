from .models import Book, Author, Category, Carousel, OrderItem, Order
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework import serializers
from .models import OTP


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['id', 'book', 'text']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True, read_only=True)
    book_author = AuthorSerializer(read_only=True)
    book_author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='book_author', write_only=True)
    book_category = CategorySerializer(read_only=True)
    book_category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='book_category', write_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'book_name', 'book_name_ru', 'book_name_en', 'book_author', 'book_author_id', 'book_category',
            'book_category_id', 'book_price', 'book_year', 'book_language', 'book_language_ru', 'book_language_en',
            'book_description', 'book_pages_count', 'book_rating', 'book_publisher',
            'book_cover'
        ]


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = BookSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    delivery_type_display = serializers.CharField(source='get_delivery_type_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'total_price', 'items',
                  'address', 'delivery_type', 'delivery_type_display', 'payment_method', 'payment_method_display',
                  'promokod', 'comment']
        read_only_fields = ['address', 'delivery_type', 'delivery_type_display',
                            'payment_method', 'payment_method_display', 'promokod', 'comment']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = self.context['request'].user
        if user != instance.user:
            for field in ['address', 'delivery_type', 'delivery_type_display',
                          'payment_method', 'payment_method_display', 'promokod', 'comment']:
                ret.pop(field, None)
        return ret


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user', 'status', 'address', 'delivery_type', 'payment_method', 'promokod', 'comment', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


class OTPCreateSerializer(serializers.ModelSerializer):
    user_phone_number = serializers.CharField(source='user.userprofile.phone_number', read_only=True)

    class Meta:
        model = OTP
        fields = ['user_phone_number', 'otp']


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
