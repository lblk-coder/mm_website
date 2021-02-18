from django.contrib import admin

from .models import Seance, Film, Projection
# Register your models here.

class ProjectionInline(admin.TabularInline):
    model = Projection
    fieldsets = [
        (None, {'fields': ['film', 'heure', 'animation']})
        ]
    extra = 0

@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    inlines = [ProjectionInline,]
    list_filter = ['date', 'lieu']
    pass

class SeanceProjectionInline(admin.TabularInline):
    model = Projection
    extra = 0

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    inlines = [SeanceProjectionInline,]
    pass