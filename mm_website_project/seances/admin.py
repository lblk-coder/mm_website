from django.contrib import admin

from .models import Seance, Film, Projection, CarouselSlider
from django.contrib.auth.models import Group

admin.site.unregister(Group)

admin.site.site_header = "Page d'administration du site de Mondes et Multitudes"

class ProjectionInline(admin.StackedInline):
    model = Projection
    fieldsets = [
        (None, {'fields': ['film', 'heure', 'animation', 'tarif', 'tarif_reduit']})
        ]
    extra = 0

@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    inlines = [ProjectionInline,]
    list_filter = ['date', 'lieu']
    list_display = ('date', 'lieu')
    ordering = ['date']
    pass

class SeanceProjectionInline(admin.StackedInline):
    model = Projection
    extra = 0

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    inlines = [SeanceProjectionInline,]
    list_display = ('titre',)
    ordering = ['titre']
    exclude = ('page_allocine',)
    change_list_template = 'admin/seances_change_list.html'
    pass

@admin.register(CarouselSlider)
class CarouselSliderAdmin(admin.ModelAdmin):
    list_display = ('date_d_ajout', 'nom')
    ordering = ['date_d_ajout']
    pass

