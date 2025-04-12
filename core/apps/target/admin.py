from django.contrib import admin

# Register your models here.
from .models import Core, DularEans, DularLinks, Mkt, Search, Curva
from django.contrib.auth.admin import UserAdmin


@admin.register(Core)
class CoreAdmin(admin.ModelAdmin):
    list_display = ('seller','name','price','url','ean','date_now')
    list_filter = ("seller", "date_now")
    ordering = ('-date_now',)
    search_fields = ('name','seller','ean')
    search_help_text = "Search by Seller, Product Name or Ean!"

@admin.register(DularEans)
class DularEansAdmin(admin.ModelAdmin):
    list_display = ('description','ean')
    search_fields = ('description','ean')


@admin.register(Curva)
class CurvaAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count', 'created_at')
    filter_horizontal = ('products',)
    search_fields = ('name','products__description','products__ean')
    search_help_text =  "Search by Product Name or Ean!"

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = "Products"

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "products":
            kwargs['queryset'] = DularEans.objects.all().only(
                'description', 'ean', 'idproduto'
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)

"""
@admin.register(Mkt)
class MktAdmin(admin.ModelAdmin):
    list_display = ('description', 'valor_nf','dular_7_a_12x', 'dular_1_a_6x','dular_1x')
"""