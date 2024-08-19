from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.conf import settings


def validate_coordinates(latitude, longitude):
    """
    Validate the given latitude and longitude coordinates.
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return True
        return False
    except ValueError:
        return False


def create_point(latitude, longitude):
    """
    Create a GeoDjango Point object from latitude and longitude.
    """
    return Point(float(longitude), float(latitude), srid=4326)


def calculate_distance(point1, point2):
    """
    Calculate the distance between two points in kilometers.
    """
    return point1.distance(point2) * 100


def perform_spatial_query(model, point, distance_km):
    """
    Perform a spatial query to find objects within a certain distance of a point.
    """
    return model.objects.filter(location__distance_lte=(point, D(km=distance_km)))


def get_nearby_objects(model, latitude, longitude, distance_km):
    """
    Get nearby objects of a specific model within a given distance.
    """
    point = create_point(latitude, longitude)
    return perform_spatial_query(model, point, distance_km).annotate(
        distance=Distance('location', point)
    ).order_by('distance')


def get_bounding_box(latitude, longitude, distance_km):
    """
    Calculate a bounding box for a given point and distance.
    """
    point = create_point(latitude, longitude)
    return point.buffer(distance_km / 111.32).extent


def format_address(street, city, state, country, postal_code):
    """
    Format address components into a single string.
    """
    return f"{street}, {city}, {state} {postal_code}, {country}"


def get_centroid(polygon):
    """
    Get the centroid of a polygon.
    """
    return polygon.centroid


def calculate_area(polygon):
    """
    Calculate the area of a polygon in square meters.
    """
    return polygon.area


def is_point_in_polygon(point, polygon):
    """
    Check if a point is within a polygon.
    """
    return polygon.contains(point)
