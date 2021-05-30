from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating')
    list_display_links = ('id', 'user')
    ordering = ('id',)


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = (PostCategoryInline,)
    list_display = ('id', 'author', 'type_post', 'title', 'get_content', 'created_at', 'rating')
    list_display_links = ('id', 'title', 'get_content',)
    ordering = ('id',)
    fields = ('author', 'type_post', 'title', 'content', 'rating')

    def get_content(self, obj):
        return ''.join((obj.content[:124], '...'))
    get_content.short_description = 'Текст'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_content', 'created_at', 'rating')
    list_display_links = ('id', 'get_content',)
    ordering = ('id', )

    def get_content(self, obj):
        return ''.join((obj.content[:64], '...'))
    get_content.short_description = 'Комментарий'


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
