from django.contrib import admin

from .models import Category, Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['description', 'category', 'published']
    list_display_links = ['description', 'category']
    search_fields = ['published']


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Category)
