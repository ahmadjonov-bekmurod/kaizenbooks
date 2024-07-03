from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorViewSet, CategoryViewSet, CommentViewSet, CarouselViewSet, OrderViewSet, \
    OTPCreateView, OTPVerifyView, UserSignUpView

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'carousels', CarouselViewSet)
router.register(r'orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('otp/create/', OTPCreateView.as_view(), name='otp-create'),
    path('otp/verify/', OTPVerifyView.as_view(), name='otp-verify'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
]
