from django.contrib import admin
from .models import Category, Post, Comment, Tag, BackgroundImage

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_on', 'status')
    list_filter = ('status', 'created_on')
    search_fields = ('title', 'author__username', 'category__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_on', 'updated_on')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    readonly_fields = ('created_on',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BackgroundImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')
    list_editable = ('is_active',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(BackgroundImage, BackgroundImageAdmin)
