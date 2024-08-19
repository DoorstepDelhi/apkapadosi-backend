from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ServiceViewSet, CategoryViewSet, SubCategoryViewSet, CollectionViewSet, BaseListingViewSet

router = DefaultRouter()
router.register(r'listings', BaseListingViewSet, basename='listing')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory')
router.register(r'collections', CollectionViewSet, basename='collection')

urlpatterns = [
    path('', include(router.urls)),
]
