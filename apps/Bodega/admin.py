from django.contrib import admin
from .models import Categoria, Figura


admin.site.site_header = 'AutoParts Bodega - Panel de Control'
admin.site.site_title = 'AutoParts Admin'
admin.site.index_title = 'Gestión de Inventario y Repuestos Automotrices'


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'activo', 'creado_en')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    list_editable = ('activo',)
    prepopulated_fields = {'slug': ('nombre',)}



@admin.register(Figura)
class FiguraAdmin(admin.ModelAdmin):
    list_display = ('slug', 'nombre', 'categoria', 'precio', 'stock', 'estado', 'activo')
    list_filter = ('categoria', 'estado', 'activo', 'destacado')
    search_fields = ('slug', 'nombre', 'fabricante', 'descripcion')
    list_editable = ('precio', 'stock', 'estado', 'activo')
    prepopulated_fields = {'slug': ('nombre',)}

    fieldsets = (
        ('Identificación y Clasificación', {
            'fields': ('nombre', 'slug', 'categoria', 'fabricante', 'escala')
        }),
        ('Detalles y Multimedia', {
            'fields': ('descripcion', 'imagen')
        }),
        ('Valores Comerciales y Estado Operativo', {
            'fields': ('precio', 'stock', 'estado', 'destacado', 'activo')
        }),
    )