from django.shortcuts import render, get_object_or_404
import datetime
from django.core.paginator import Paginator
from .models import Film, Seance, Projection
from .forms import FormSeances

def home(request):
    seances = []  # une liste de séances vide
    today = datetime.date.today()  # ici et dessous on compare si la séance est passée ou pas
    for seance in Seance.objects.all().order_by('date'):
        if seance.date >= today:
            seances.append(seance)  # si séance pas passée, on l'ajoute à la liste
    paginator = Paginator(seances, 5)  # pour ne présenter que 5 séances max sur la page d'accueil
    page_obj = paginator.page(request.GET.get('page', '1'))
    #  la section ci-dessous est à retravailler pour mettre un catalogue proprement
    try:  # TODO mettre possibilité d'uploader un catalogue ici... il faut qu'on voit sa couverture... C'EST CHAUD !!!!
        catalogue_img = Film.objects.get(title="catalogue").picture  # it bugs here when I run a unittest, maybe it comes from the fact that it is a static file...
    except:
        catalogue_img = ''
        pass
    #  fin de la section à retravailler
    context = {
        'seances' : seances,
        'page_obj' : page_obj,
        'catalogue_img' : catalogue_img,
    }
    return render(request, 'seances/home.html', context)

def listing(request): #  this view returns all the screenings in the dbase + research form
    query = request.GET.get('query')
    if query:
        seances = []
        form = FormSeances(request.GET)
        if form.is_valid():
            lieu = str(form.cleaned_data['Lieu'])  #getting the data form the form, converting it in str
            lieu = lieu[2:-2]  #keeping only the part of the string we want
            date = str(form.cleaned_data['Date'])
            date = date[2:-2]
            films = str(form.cleaned_data['Film'])
            films = films[2:-2]
            if lieu and date and films:  # i did not find a better way of coding this filter mechanism, TODO find a better way with less code!
                films = Film.objects.get(title=films)
                seances = Seance.objects.filter(location=lieu, date=date, films=films)
            if lieu and date and not films:  # 2
                seances = Seance.objects.filter(location=lieu, date=date)
            if lieu and films and not date:  # 2
                films = Film.objects.get(title=films)
                seances = Seance.objects.filter(location=lieu, films=films)
            if date and films and not lieu:  # 2
                films = Film.objects.get(title=films)
                seances = Seance.objects.filter(films=films, date=date)
            if date and not films and not lieu:
                seances = Seance.objects.filter(date=date)
            if films and not date and not lieu:
                films = Film.objects.get(title=films)
                seances = Seance.objects.filter(films=films)
            if lieu and not films and not date:
                seances = Seance.objects.filter(location=lieu)
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
        films = Film.objects.all().order_by('titre')
        context = {
        'seances' : seances,
        'films' : films,
        'form' : form,
    }
        return render(request, 'seances/listing.html', context)

def detail(request, film_id):  #  this view shows every parameters a particular screening has
    film = get_object_or_404(Film, pk=film_id)
    context = {
        'film': film,
    }
    return render(request, 'seances/detail.html', context)