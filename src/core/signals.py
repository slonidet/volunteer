from django.db.models import FileField


def file_field_delete(sender, instance, **kwargs):
    """ Delete attachment from the file system """
    for field in sender._meta.fields:
        if isinstance(field, FileField):
            getattr(instance, field.name).delete(False)
