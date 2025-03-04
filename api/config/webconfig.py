from django.utils import timezone

IS_LOCAL_HOST = False

# API_URL  = "http://127.0.0.1:8000/api/v1/" if IS_LOCAL_HOST else "https://server.cyanase.lol/api/v1/"
# BASE_URL = "http://127.0.0.1:8000/" if IS_LOCAL_HOST else "https://server.cyanase.lol/"
API_URL  = "http://127.0.0.1:8000/api/v1/" if IS_LOCAL_HOST else "https://server.cyanase.app/api/v1/"
BASE_URL = "http://127.0.0.1:8000/" if IS_LOCAL_HOST else "https://server.cyanase.app/"

ID_ENCRYPTION_KEY = "ADB-KJQ-FZY-TQYJ"

# Required Dimensions
max_thumbnail_width = 1200
max_thumbnail_height = 700

sizes = [
    # mobile/desktop display image results
    {"width": 1920, "height": 1080},  # view large slide
    {"width": 1280, "height": 720}, 
    {"width": 854, "height": 480},  # standard image thumbnails
    {"width": 640, "height": 360},  # web courasel selector image
]

# Device poster resolutions
DEFAULT_MOBILE_IMAGE_RESOLUTION = "640x360"
DEFAULT_TABLATE_IMAGE_RESOLUTION = "854x480"
DEFAULT_DESKTOP_IMAGE_SM_RESOLUTION = "854x480"
DEFAULT_DESKTOP_IMAGE_XS_RESOLUTION = "640x360"
DEFAULT_DESKTOP_IMAGE_LG_RESOLUTION = "1280x720"
DEFAULT_DESKTOP_IMAGE_XL_RESOLUTION = "1920x1080"
# Required Image Extensions
valid_image_extensions = [".jpg", ".png"]
# valid valid video extensions
############
# PAGINATION
############
results_per_page = 25
# Timezones
default_date_time = timezone.now()
# Email config
SMTP_USENAME = "no-reply@cyanase.com"
SMTP_PASSWORD = "xxxxxxxxxxxxxx"
SMTP_SERVER = "mail.cyanase.com"
SMTP_PORT = 587
