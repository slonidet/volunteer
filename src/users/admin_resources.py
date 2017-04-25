from import_export.resources import ModelResource

from users.models import Profile


class ProfileAdminResource(ModelResource):
    def get_export_headers(self):
        exported_fields = super().get_export_headers()
        return [field.verbose_name.title()
                for field in self.Meta.model._meta.fields
                if field.name in exported_fields]

    class Meta:
        model = Profile
