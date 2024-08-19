from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('api/search/', search_listings, name='search-listings'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('accounts.urls')),
    path('', include('entities.urls')),
    path('', include('listings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
