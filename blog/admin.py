from django.contrib import admin
from blog.models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'views_count')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}  # Это для автоматической генерации slug из title

admin.site.register(Blog, BlogAdmin)