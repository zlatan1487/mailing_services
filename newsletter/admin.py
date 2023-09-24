from django.contrib import admin
from newsletter.models import Customer, Mailing, MailText, MailingLog


# Администрирование модели Customer (Клиенты)
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')


# Администрирование модели Mailing (Рассылки)
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')

    def get_clients(self, obj):
        return ", ".join([str(client) for client in obj.clients.all()])

    get_clients.short_description = 'Клиенты'


# Администрирование модели MailText (Тексты сообщений)
@admin.register(MailText)
class MailTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'message')


# Администрирование модели MailingLog (Логи рассылки)
@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'server_response', 'timestamp')
