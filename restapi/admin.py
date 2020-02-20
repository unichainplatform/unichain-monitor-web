from django.contrib import admin
from restapi.models import AccountModel, HostsModel


@admin.register(AccountModel)
class AccountModeldmin(admin.ModelAdmin):
    list_display = ('id', 'public_key')


@admin.register(HostsModel)
class HostsModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'user', 'password')