from django.contrib import admin

# Register your models here.
from .models import Core, DularEans, DularLinks, Mkt, Search
from django.contrib.auth.admin import UserAdmin


@admin.register(Core)
class CoreAdmin(admin.ModelAdmin):
    list_display = ('seller','name','price','url','ean','date_now')
    list_filter = ("seller", "date_now")
    ordering = ('-date_now',)
    search_fields = ('name','seller','ean')

@admin.register(DularEans)
class DularEansAdmin(admin.ModelAdmin):
    list_display = ('description','ean')
    search_fields = ('description','ean')

"""
@admin.register(Mkt)
class MktAdmin(admin.ModelAdmin):
    list_display = ('description', 'valor_nf','dular_7_a_12x', 'dular_1_a_6x','dular_1x')
"""