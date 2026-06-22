from django.contrib import admin

from crm.models import (
    Category,
    Supplier,
    Unit,
    ProductGroup,
    Product,
    Campaign,
    ExportCategory,
    ClientCategory,
    Client,
    Deal,
    Interaction,
    Notification,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('title', 'fio', 'phone')
    search_fields = ('title', 'fio', 'phone')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'price')
    list_filter = ('group',)
    search_fields = ('title',)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'start_at', 'end_at')
    list_filter = ('product',)
    search_fields = ('title',)
    date_hierarchy = 'start_at'


@admin.register(ExportCategory)
class ExportCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(ClientCategory)
class ClientCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('title', 'fio', 'phone', 'email', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'fio', 'email', 'phone')


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('client', 'product', 'count', 'date', 'export_category')
    list_filter = ('export_category', 'date')
    search_fields = ('client__title', 'product__title')
    date_hierarchy = 'date'


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'title', 'status', 'created_at')
    list_filter = ('type', 'status')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'date', 'is_hidden')
    list_filter = ('is_hidden', 'date')
    search_fields = ('user__username', 'text')
