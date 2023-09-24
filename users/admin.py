from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_blocked')  # Поля, которые будут отображаться в списке пользователей в админке
    list_filter = ('is_blocked',)  # Добавьте фильтр по полю 'is_blocked'
    actions = ['block_users', 'unblock_users']  # Действия для блокировки и разблокировки пользователей

    def block_users(self, request, queryset):
        queryset.update(is_blocked=True)
    block_users.short_description = 'Блокировать выбранных пользователей'

    def unblock_users(self, request, queryset):
        queryset.update(is_blocked=False)
    unblock_users.short_description = 'Разблокировать выбранных пользователей'

admin.site.register(User, UserAdmin)
