from django.contrib import admin
from django.forms import TextInput, Textarea
from django.template.defaultfilters import truncatechars
from django.db import models
from app_news.models import News, Comments, Profile


class CommentInLine(admin.TabularInline):
    model = Comments
    extra = 0


class NewAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'flag_active']
    list_filter = ['flag_active']
    inlines = [CommentInLine]

    actions = ['mark_is_active', 'mark_is_not_active']

    def mark_is_active(self, request, queryset):
        queryset.update(flag_active='a')

    def mark_is_not_active(self, request, queryset):
        queryset.update(flag_active='n')

    mark_is_active.short_description = 'Перевести в статус Активно'
    mark_is_not_active.short_description = 'Перевести в статус Не активно'


class CommentAdmin(admin.ModelAdmin):
    model = Comments
    list_display = ['name', 'short_text', 'news']
    list_filter = ['name']

    def short_text(self, obj):
        return truncatechars(obj.text, 15)

    actions = ['delete_comment']

    def delete_comment(self, request, queryset):
        queryset.update(text='Удалено администратором')

    delete_comment.short_description = 'Удалить комментарий'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'flag_verification']

    actions = ['mark_is_active', 'mark_is_not_active']

    def mark_is_active(self, request, queryset):
        queryset.update(flag_verification=True)

    def mark_is_not_active(self, request, queryset):
        queryset.update(flag_verification=False)

    mark_is_active.short_description = 'Перевести в статус Верифицирован'
    mark_is_not_active.short_description = 'Перевести в статус Не верифицирован'


admin.site.register(Profile, ProfileAdmin)
admin.site.register(News, NewAdmin)
admin.site.register(Comments, CommentAdmin)
