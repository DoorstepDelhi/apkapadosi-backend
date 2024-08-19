from django.urls import path, include
from rest_framework.routers import DefaultRouter
from entities.views import EntityViewSet

router = DefaultRouter()
router.register(r'entities', EntityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('entities/<int:pk>/add_product/', EntityViewSet.as_view({'post': 'add_product'}), name='entity-add-product'),
    # path('entities/<int:pk>/add_service/', EntityViewSet.as_view({'post': 'add_service'}), name='entity-add-service'),
    # path('entities/search/', EntityViewSet.as_view({'get': 'search'}), name='entity-search'),
    # path('entities/<int:pk>/add_user/', EntityViewSet.as_view({'post': 'add_user'}), name='entity-add-user'),
    # path('entities/<int:pk>/update_details/', EntityViewSet.as_view({'post': 'update_details'}), name='entity-update-details'),
    # path('entities/<int:pk>/add_media/', EntityViewSet.as_view({'post': 'add_media'}), name='entity-add-media'),
    # path('entities/<int:pk>/products/', EntityViewSet.as_view({'get': 'products'}), name='entity-products'),
    # path('entities/<int:pk>/services/', EntityViewSet.as_view({'get': 'services'}), name='entity-services'),
]