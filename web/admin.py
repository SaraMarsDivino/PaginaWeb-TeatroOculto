from django.contrib import admin
from .models import Obra, Iniciativa, Equipo, Suscriptor, MensajeContacto


@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'release_date', 'active')
	list_filter = ('active',)
	search_fields = ('title', 'slug', 'synopsis')


@admin.register(Iniciativa)
class IniciativaAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'category', 'created_at')
	list_filter = ('category',)
	search_fields = ('title', 'slug', 'description')


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'role', 'order')
	ordering = ('order',)


@admin.register(Suscriptor)
class SuscriptorAdmin(admin.ModelAdmin):
	list_display = ('email', 'name', 'age', 'created_at')
	search_fields = ('email', 'name')


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'created_at')
	search_fields = ('name', 'email', 'message')
