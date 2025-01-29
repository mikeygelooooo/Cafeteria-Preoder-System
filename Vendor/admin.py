from django.contrib import admin
from .models import Stall, Vendor

# Register your models here.
@admin.register(Stall)
class StallAdmin(admin.ModelAdmin):
    list_display = ('stall_no', 'stall_name', 'is_open', 'opening_time', 'closing_time')
    search_fields = ('stall_name',)
    list_filter = ('is_open',)

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'stall',)
    search_fields = ('user__first_name', 'user__last_name', 'stall__stall_name')
    list_filter = ('stall',)