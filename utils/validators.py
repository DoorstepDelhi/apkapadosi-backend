from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.geos import Point
import re

def validate_coordinates(latitude, longitude):
    try:
        point = Point(float(longitude), float(latitude))
        if not (-90 <= point.y <= 90) or not (-180 <= point.x <= 180):
            raise ValidationError(_("Invalid coordinates. Latitude must be between -90 and 90, and longitude between -180 and 180."))
    except (ValueError, TypeError):
        raise ValidationError(_("Invalid coordinate format. Please provide valid numbers for latitude and longitude."))

def validate_phone_number(value):
    phone_regex = re.compile(r'^\+?1?\d{9,15}$')
    if not phone_regex.match(value):
        raise ValidationError(_("Invalid phone number format. Please use a valid international format."))

def validate_website_url(value):
    url_regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if not url_regex.match(value):
        raise ValidationError(_("Invalid URL format. Please provide a valid URL."))

def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError(_('File too large. Size should not exceed 5 MB.'))

def validate_image_file(value):
    validate_file_size(value)
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
    ext_validator = FileExtensionValidator(allowed_extensions=valid_extensions)
    try:
        ext_validator(value)
    except ValidationError:
        raise ValidationError(_("Unsupported image format. Please use JPG, JPEG, PNG, or GIF."))

def validate_video_file(value):
    validate_file_size(value)
    valid_extensions = ['mp4', 'avi', 'mov', 'wmv']
    ext_validator = FileExtensionValidator(allowed_extensions=valid_extensions)
    try:
        ext_validator(value)
    except ValidationError:
        raise ValidationError(_("Unsupported video format. Please use MP4, AVI, MOV, or WMV."))

def validate_document_file(value):
    validate_file_size(value)
    valid_extensions = ['pdf', 'doc', 'docx', 'txt']
    ext_validator = FileExtensionValidator(allowed_extensions=valid_extensions)
    try:
        ext_validator(value)
    except ValidationError:
        raise ValidationError(_("Unsupported document format. Please use PDF, DOC, DOCX, or TXT."))

def validate_price(value):
    if value < 0:
        raise ValidationError(_("Price cannot be negative."))

def validate_rating(value):
    if not 1 <= value <= 5:
        raise ValidationError(_("Rating must be between 1 and 5."))

def validate_category_name(value):
    if len(value) < 2 or len(value) > 50:
        raise ValidationError(_("Category name must be between 2 and 50 characters long."))

def validate_collection_name(value):
    if len(value) < 2 or len(value) > 100:
        raise ValidationError(_("Collection name must be between 2 and 100 characters long."))