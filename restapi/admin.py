from django.contrib import admin
from restapi.models import Accounts, Hosts


@admin.register(Accounts)
class Accountsdmin(admin.ModelAdmin):
    list_display = ('id', 'public_key')


@admin.register(Hosts)
class HostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'user', 'password')