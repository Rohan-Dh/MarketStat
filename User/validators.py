from django.core.exceptions import ValidationError
from PIL import Image

def validateImage(image):
    try:
        img = Image.open(image)
    except Exception:
        print("invalid image file")
        raise ValidationError("Invalid image file")
    
    if img.format.lower() not in ['jpeg', 'png', 'jpg']:
        print("invalid image format")
        raise ValidationError("Unsupported image format. Allowed formats: JPEG, PNG")
    
    if image.size > 5 * 1024 * 1024:
        print("size invalid")
        raise ValidationError("Image size exceeds the limit of 5MB.")