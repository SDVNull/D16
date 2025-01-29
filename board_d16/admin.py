from django.contrib import admin
from .models import Advertisement, Response


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_filter = ('category', 'author__is_staff')

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'author', 'content', 'created_at', 'adopted')
    search_fields = ('advertisement__title', 'author__username')
    list_filter = ('adopted', 'created_at')


