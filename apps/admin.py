from django.contrib import admin

from .models import Post, PostMedia, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone', 'birthday', 'is_archive']
    search_fields = ['username', 'phone']
    list_filter = ['username']


class PostMediaInline(admin.StackedInline):
    model = PostMedia
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'post_type', 'views', 'created_at', 'id']
    search_fields = ['post_type']
    list_filter = ['post_type']
    inlines = [PostMediaInline, ]


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ['post', 'media_type', 'file']

