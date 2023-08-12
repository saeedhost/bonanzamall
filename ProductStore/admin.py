from django.contrib import admin
from ProductStore.models import Store_Product, Top_Product, Special_Offer, Comment
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

class TopProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_short_description', 'actual_price', 'list_price', 'percent_off', 'main_image_link', 'sub_image_link_2', 'sub_image_link_3', 'sub_image_link_4', 'product_long_description', 'product_specification', 'product_category', 'product_quantity')

class SpecialOffersAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_short_description', 'actual_price', 'list_price', 'percent_off', 'main_image_link', 'sub_image_link_2', 'sub_image_link_3', 'sub_image_link_4', 'product_long_description', 'product_specification', 'product_category', 'product_quantity')

class StoreProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_short_description', 'actual_price', 'list_price', 'percent_off', 'main_image_link', 'sub_image_link_2', 'sub_image_link_3', 'sub_image_link_4', 'product_long_description', 'product_specification', 'product_category', 'product_quantity')

admin.site.register(Top_Product, TopProductsAdmin)
admin.site.register(Special_Offer, SpecialOffersAdmin)
admin.site.register(Store_Product, StoreProductsAdmin)

class CommentInline(GenericTabularInline):
    model = Comment
    extra = 0

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_content_object_name', 'content', 'rating', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content')
    readonly_fields = ('created_at',)
    
    def get_content_object_name(self, obj):
        return str(obj.content_object)
    
    get_content_object_name.short_description = 'Product'
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('user', 'content_type', 'object_id', 'content', 'image', 'rating', 'created_at'),
        }),
    )
