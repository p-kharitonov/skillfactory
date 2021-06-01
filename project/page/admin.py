from django.contrib import admin
from .models import Page, Category


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'update_at')
    list_display_links = ('id', 'title')
    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        if not change:  # Проверяем что запись только создаётся
            obj.author = request.user  # Присваеваем полю автор текущего пользователя

        super(PageAdmin, self).save_model(
            request=request,
            obj=obj,
            form=form,
            change=change
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)

