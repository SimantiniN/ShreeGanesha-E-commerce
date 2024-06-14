from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display=('email','first_name','last_name','username','joined_date','last_login','is_active')
    list_display_links=('email','first_name','last_name')
    readonly_fields=('joined_date','last_login')
    ordering=('-joined_date',)
    filter_horizontal=()
    list_filter=()
    fieldsets=()
admin.site.register(Account,AccountAdmin)
