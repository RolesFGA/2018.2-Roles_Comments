from django.contrib import admin

# Register your models here.
from .models import Vote


admin.site.register(
    Vote,
    raw_id_fields=["user"],
    list_filter=["create_at"],
    list_display=["user", "content_object", "create_at"],
    search_fields=["user__username", "user__email"]
)
