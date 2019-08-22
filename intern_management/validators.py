from django.core.exceptions import ValidationError
from django.conf import settings


def validate_image_size(image):
    filesize = image.file.size
    max_upload_size = settings.MAX_FILE_SIZE
    print(image.file.size)
    if filesize > max_upload_size*(1024**2):
        raise ValidationError(
            "Max file upload size is {}".format(max_upload_size)
        )
