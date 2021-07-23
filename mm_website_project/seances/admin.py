from django.contrib import admin
from .models import Seance, Film, Projection, CarouselSlider
from django.contrib.auth.models import Group
from django.urls import path
from seances.forms import ScrapyForm
from django.template.response import TemplateResponse

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

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('scrap_film_nfos/', self.scrap_film_nfos),
        ]
        return my_urls + urls

    def scrap_film_nfos(self, request):
        if request.method == 'GET':
            scrapy_form = ScrapyForm()
            fichier = open('fichier1.txt', 'w')
            fichier.write(str('get'))
            fichier.close()
        elif request.method == 'POST':
            scrapy_form = ScrapyForm(request.POST)
            fichier = open('fichier2.txt', 'w')
            fichier.write(str('post'))
            fichier.close()
            if scrapy_form.is_valid():
                url = scrapy_form.cleaned_data['film_url']
                reponse = requests.get(url)
                soup = BeautifulSoup(reponse.text, 'html.parser')

                # below is the regex to find the date
                date_regex = r"^[A-Za-z0-9._ =-]*date blue-link$"
                # compile the regex, I don't really understand why it matters yet...
                date_srch = re.compile(date_regex)

                # select the precise part of the <span> we're interested in
                # since there are some spare spaces before and after the date.
                for elt in soup.find_all('span', date_srch):
                    date = elt.string[-21:-17]
                if not date:
                    date = soup.find_all('span', 'date')[0].string[-4:]

                # this is a function we develop to get everything there is in this script
                # it find the only script that contains the word "duration" in its string
                def getinfos():
                    for elt in soup.find_all('script'):
                        try:
                            result = re.search('duration', elt.string)
                        except:
                            continue
                        if result:
                            return result

                # we use the function defined above to get raw infos
                # then we split it to have separated strings to iter
                # within.
                infos = getinfos()
                splitted_infos = infos.string.split()

                # this function will remove commas and brackets from extracted infos
                # that we got from the html strings.
                def remove_commas_and_brackets(word):
                    word = word.replace(",", "")
                    word = word.replace('"', "")
                    return word

                # below, we extract each separate infos
                i = 0
                # these boolean below exist to keep only first iteration
                # of info (since there might be the same elsewhere in the html
                # page, without the same presentation).
                name_bool = False
                duree_bool = False
                genre_bool = False
                descrip_bool = False
                dir_bool = False
                act_bool = False
                for elt in splitted_infos:
                    if elt == '"name":' and name_bool == False:  # titre
                        name_bool = True
                        titre = splitted_infos[i][8:-2]
                    elif elt == '"duration":' and duree_bool == False:  # durée
                        duree_bool = True
                        duree = splitted_infos[i + 1][3:8]
                        duree = (int(duree[1]) * 60) + int(duree[-2::])  # converting duration from
                        # HH:MM to minutes only.
                    elif elt == '"genre":' and genre_bool == False:  # genre
                        genre_bool = True
                        i2 = i + 2
                        genre = ''
                        genre += remove_commas_and_brackets(splitted_infos[i2]) + ", "
                        while splitted_infos[i2 + 1] != ']':
                            i2 += 1
                            genre += remove_commas_and_brackets(splitted_infos[i2])
                            if splitted_infos[i2 + 1] != ']':
                                genre += ', '
                    elif elt == '"description":' and descrip_bool == False:  # synopsis
                        descrip_bool = True
                        i1 = i + 1
                        synopsis = ''
                        synopsis += remove_commas_and_brackets(splitted_infos[i1]) + " "
                        while splitted_infos[i1 + 1] != '"director":':
                            i1 += 1
                            synopsis += remove_commas_and_brackets(splitted_infos[i1]) + " "
                        synopsis = synopsis[:-2]
                    elif elt == '"director":' and dir_bool == False:  # réalisateur.rice
                        dir_bool = True
                        i7 = i + 7
                        director = ''
                        while splitted_infos[i7] != '}':
                            director += remove_commas_and_brackets(splitted_infos[i7]) + " "
                            i7 += 1
                        director = director[:-1]
                    elif elt == '"actor":' and act_bool == False:  # acteur.rice.s
                        act_bool = True
                        i8 = i + 8
                        actors = ''
                        end = False
                        while end == False:
                            while splitted_infos[i8] != '},' and splitted_infos[i8] != '}':
                                actors += remove_commas_and_brackets(splitted_infos[i8]) + " "
                                i8 += 1
                            actors = actors[:-1] + ", "
                            if splitted_infos[i8 + 1] == ']':
                                end = True
                            i8 += 7
                        actors = actors[:-2]
                    i += 1
                Film.objects.create(
                    titre=titre,
                    real=director,
                    acteurs=actors,
                    genre=genre,
                    annee=date,
                    duree=duree,
                    synopsis=synopsis,
                )
        else:
            fichier = open('fichier3.txt', 'w')
            fichier.write(str('get'))
            fichier.close()
        context = dict(
            self.admin_site.each_context(request),
            scrapy_form = scrapy_form,
        )
        return TemplateResponse(request, "admin/seances_change_list.html", context)

@admin.register(CarouselSlider)
class CarouselSliderAdmin(admin.ModelAdmin):
    list_display = ('date_d_ajout', 'nom')
    ordering = ['date_d_ajout']
    pass

