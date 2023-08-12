from django.contrib import admin
from CustomerOrders.models import CustomerBilling, CustomerBillingItem

class CustomerBillingItemInline(admin.TabularInline):
    model = CustomerBillingItem
    extra = 1

class CustomerBillingAdmin(admin.ModelAdmin):
    inlines = [CustomerBillingItemInline]
    list_display = ('invoice_number','fullname', 'email', 'province', 'district', 'mobile_number', 'address', 'created_at')
    search_fields = ('invoice_number', 'fullname', 'email')
    
admin.site.register(CustomerBilling, CustomerBillingAdmin)


