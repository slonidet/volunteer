from django.db.models.signals import pre_delete

from core.signals import file_field_delete
from gallery.models import Photo


pre_delete.connect(file_field_delete, Photo)
