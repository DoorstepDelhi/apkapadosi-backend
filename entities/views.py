from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Entity, EntityUser, EntityMedia
from .serializers import EntitySerializer, EntityListSerializer, EntityUserSerializer, EntityMediaSerializer
from listings.models import Listing, Service
from listings.serializers import ListingSerializer, ServiceSerializer
from utils.permissions import IsEntityAdmin, IsEntityCollaborator
from utils.validators import validate_coordinates

class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return EntityListSerializer
        return EntitySerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsEntityAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        entity = serializer.save()
        EntityUser.objects.create(entity=entity, user=self.request.user, role='admin', is_creator=True)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsEntityCollaborator])
    def add_product(self, request, pk=None):
        entity = self.get_object()
        listing_data = request.data
        listing_data['vendor'] = entity.id
        listing_data['listing_type'] = 'product'
        serializer = ListingSerializer(data=listing_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsEntityCollaborator])
    def add_service(self, request, pk=None):
        entity = self.get_object()
        service_data = request.data
        service_data['vendor'] = entity.id
        serializer = ServiceSerializer(data=service_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        radius = request.query_params.get('radius', 10)  # Default radius: 10km

        queryset = self.get_queryset()

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(deals_in__icontains=query)
            )

        if lat and lon:
            try:
                lat, lon = validate_coordinates(lat, lon)
                user_location = Point(float(lon), float(lat), srid=4326)
                queryset = queryset.annotate(
                    distance=Distance('location', user_location)
                ).filter(location__distance_lte=(user_location, D(km=radius)))
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EntityListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_user(self, request, pk=None):
        entity = self.get_object()
        user_data = request.data
        user_data['entity'] = entity.id
        serializer = EntityUserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_details(self, request, pk=None):
        entity = self.get_object()
        serializer = EntitySerializer(entity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_media(self, request, pk=None):
        entity = self.get_object()
        media_data = request.data
        media_data['entity'] = entity.id
        serializer = EntityMediaSerializer(data=media_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        entity = self.get_object()
        products = Listing.objects.filter(vendor=entity, listing_type='product')
        serializer = ListingSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        entity = self.get_object()
        services = Service.objects.filter(listing__vendor=entity)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)