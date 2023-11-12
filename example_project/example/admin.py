from django.contrib import admin

from .models import Blob


class ExampleAdmin(admin.ModelAdmin):
    list_display = ("__str__",)


admin.site.register(Blob, ExampleAdmin)
