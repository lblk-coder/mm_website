from django.shortcuts import render, get_object_or_404, redirect
import datetime
import pytz
from django.core.paginator import Paginator
from .models import Film, Seance, Projection, CarouselSlider
from .forms import FormSeances, ScrapyForm

# below are the imports for scrapping view
from bs4 import BeautifulSoup
import requests
import re
import pickle
import json
import time
import os

def home(request):
    seances = []  # une liste de séances vide
    today = datetime.date.today()  # ici et dessous on compare si la séance est passée ou pas
    for seance in Seance.objects.all().order_by('date'):
        if seance.date >= today:
            seances.append(seance)  # si séance pas passée, on l'ajoute à la liste
    paginator = Paginator(seances, 6)  # pour ne présenter que 6 séances max sur la page d'accueil
    page_obj = paginator.page(request.GET.get('page', '1'))
    context = {
        'seances' : seances,
        'page_obj' : page_obj,
    }
    return render(request, 'seances/home.html', context)

def listing(request, populated=0, seance_id=None): #  this view returns all the screenings in the dbase + research form
    for elt in Seance.objects.all():
        #  comparing seance's date (converted into an aware datetime.datetime object,
        #  with 23h59 set as time so the seance disapears only the day after)
        #  with timezone aware datetime.datetime."now" object, set on UTC+2 (Paris)
        if datetime.datetime(elt.date.year, elt.date.month, elt.date.day, 23, 59,
                             tzinfo=pytz.timezone('Europe/Paris')) < pytz.utc.localize(datetime.datetime.utcnow()).astimezone(pytz.timezone('Europe/Paris')):
            elt.delete()
    query = request.GET.get('query')
    if populated == '1':  # populated == 1 when a seance is clicked on, on the home page. It populates the form
        # with this particular seance's date and location.
        query = True
        request.GET = request.GET.copy()
        request.GET['Lieu'] = Seance.objects.get(pk=seance_id).lieu
        request.GET['Date'] = Seance.objects.get(pk=seance_id).date
    if query:
        seances = []
        form = FormSeances(request.GET)
        if form.is_valid():
            lieu = str(form.cleaned_data['Lieu'])  #getting the data form the form, converting it in str
            date = str(form.cleaned_data['Date'])
            film = str(form.cleaned_data['Film'])
            if lieu and date and film:  # i did not find a better way of coding this filter mechanism
                seances = Seance.objects.filter(lieu=lieu,
                                                date=date,
                                                projection__film__titre=film).order_by('date')
            if lieu and date and not film:  # 2
                seances = Seance.objects.filter(lieu=lieu, date=date).order_by('date')
            if lieu and film and not date:  # 2
                seances = Seance.objects.filter(lieu=lieu, projection__film__titre=film).order_by('date')
            if date and film and not lieu:  # 2
                seances = Seance.objects.filter(date=date, projection__film__titre=film).order_by('date')
            if date and not film and not lieu:
                seances = Seance.objects.filter(date=date).order_by('date')
            if film and not date and not lieu:
                seances = Seance.objects.filter(projection__film__titre=film).order_by('date')
            if lieu and not film and not date:
                seances = Seance.objects.filter(lieu=lieu).order_by('date')
            if len(seances) == 0:
                message = "Désolé, il n'existe aucune séance correspondant à ces critères !"
            else:
                message = ""
            form = FormSeances()
            context = {
                'seances' : seances,
                'message' : message,
                'form' : form,
            }
            return render(request, 'seances/listing.html', context)
        else:
            form = FormSeances()
            seances = Seance.objects.all().order_by('date')
            film = Film.objects.all().order_by('titre')
            context = {
                'seances': seances,
                'film': film,
                'form': form,
            }
            return render(request, 'seances/listing.html', context)
    else:
        form = FormSeances()
        seances = Seance.objects.all().order_by('date')
        film = Film.objects.all().order_by('titre')
        context = {
        'seances' : seances,
        'film' : film,
        'form' : form,
    }
        return render(request, 'seances/listing.html', context)

def detail(request, film_id):  #  this view shows every parameters a particular screening has
    film = get_object_or_404(Film, pk=film_id)
    projections = film.projection_set.all().order_by('seance__date')
    context = {
        'film': film,
        'projections': projections,
    }
    return render(request, 'seances/detail.html', context)

def content(request, value):
    if int(value) == 0:
        return render(request, 'seances/content/asso.html')
    elif int(value) == 1:
        return render(request, 'seances/content/equipe.html')
    elif int(value) == 2:
        return render(request, 'seances/content/conseil.html')
    elif int(value) == 3:
        return render(request, 'seances/content/partenaires.html')
    elif int(value) == 4:
        return render(request, 'seances/content/contact.html')
    elif int(value) == 5:
        return render(request, 'seances/content/emploi.html')
    elif int(value) == 6:
        return render(request, 'seances/content/rejoindre.html')
    elif int(value) == 8:
        return render(request, 'seances/content/plein-air.html')
    elif int(value) == 9:
        return render(request, 'seances/content/seniors.html')
    elif int(value) == 10:
        return render(request, 'seances/content/patrimoine.html')
    elif int(value) == 11:
        return render(request, 'seances/content/spectacles.html')
    elif int(value) == 12:
        return render(request, 'seances/content/seances-militantes.html')
    elif int(value) == 13:
        return render(request, 'seances/content/louise.html')
    elif int(value) == 14:
        return render(request, 'seances/content/scolaires.html')
    elif int(value) == 15:
        return render(request, 'seances/content/ecole-college.html')
    elif int(value) == 16:
        return render(request, 'seances/content/lyceens-apprentis.html')
    elif int(value) == 17:
        return render(request, 'seances/content/festival.html')

# this view gets the infos of a film from its allociné page
def scrap_film_nfos(request):
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
    else :
        fichier = open('fichier3.txt', 'w')
        fichier.write(str('get'))
        fichier.close()
    context = {
        'scrapy_form': scrapy_form,
    }
    return context