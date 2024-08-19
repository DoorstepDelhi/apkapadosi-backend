from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .models import Listing, Category, Collection
from .serializers import ListingSerializer, CategorySerializer, CollectionSerializer

class BaseListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()  # Add a default queryset

    def get_queryset(self):
        # Override get_queryset to filter based on listing_type
        return self.queryset.filter(listing_type=self.listing_type)

    @action(detail=True, methods=['post'])
    def add_to_collection(self, request, pk=None):
        listing = self.get_object()
        collection_id = request.data.get('collection_id')
        try:
            collection = Collection.objects.get(id=collection_id)
            collection.listings.add(listing)
            return Response({'status': f'{self.listing_type.capitalize()} added to collection'}, status=status.HTTP_200_OK)
        except Collection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        listings = self.queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
        serializer = self.get_serializer(listings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def media_upload(self, request, pk=None):
        listing = self.get_object()
        image = request.data.get('image')
        if image:
            listing.images.create(image_url=image, image_alt_text=request.data.get('alt_text', ''))
            return Response({'status': 'Media uploaded'}, status=status.HTTP_200_OK)
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

class ProductViewSet(BaseListingViewSet):
    queryset = Listing.objects.filter(listing_type='product')
    listing_type = 'product'

class ServiceViewSet(BaseListingViewSet):
    queryset = Listing.objects.filter(listing_type='service')
    listing_type = 'service'

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(parent_category__isnull=True)
    serializer_class = CategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(parent_category__isnull=False)
    serializer_class = CategorySerializer

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        collection = self.get_object()
        listings = collection.listings.all()
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)
