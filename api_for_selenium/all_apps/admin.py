from django.contrib import admin
from all_apps.models import OthersField
from django.contrib.auth.models import Group

# Register your models here.

class UserGridAdmin(admin.ModelAdmin):

    list_display = ['address', 'phone_number']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs:
            qs = qs.filter(user__is_superuser=False)
        return qs

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



admin.site.register(OthersField, UserGridAdmin)
admin.site.unregister(Group)