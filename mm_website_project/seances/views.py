from django.shortcuts import render, get_object_or_404
import datetime
from django.core.paginator import Paginator
from .models import Film, Seance, Projection, Catalogue
from .forms import FormSeances

def home(request):
    seances = []  # une liste de séances vide
    today = datetime.date.today()  # ici et dessous on compare si la séance est passée ou pas
    for seance in Seance.objects.all().order_by('date'):
        if seance.date >= today:
            seances.append(seance)  # si séance pas passée, on l'ajoute à la liste
    paginator = Paginator(seances, 5)  # pour ne présenter que 5 séances max sur la page d'accueil
    page_obj = paginator.page(request.GET.get('page', '1'))
    catalogue_cover = Catalogue.objects.get(home_page=True).couverture
    catalogue_link = Catalogue.objects.get(home_page=True).catalogue
    context = {
        'seances' : seances,
        'page_obj' : page_obj,
        'catalogue_cover' : catalogue_cover,
        'catalogue_link' : catalogue_link,
    }
    return render(request, 'seances/home.html', context)

def listing(request): #  this view returns all the screenings in the dbase + research form
    query = request.GET.get('query')
    if query:
        seances = []
        form = FormSeances(request.GET)
        if form.is_valid():
            lieu = str(form.cleaned_data['Lieu'])  #getting the data form the form, converting it in str
            date = str(form.cleaned_data['Date'])
            film = str(form.cleaned_data['Film'])
            if lieu and date and film:  # i did not find a better way of coding this filter mechanism, TODO find a better way with less code!
                seances = Seance.objects.filter(lieu=lieu, date=date, projection__film__titre=film)
            if lieu and date and not film:  # 2
                seances = Seance.objects.filter(lieu=lieu, date=date)
            if lieu and film and not date:  # 2
                seances = Seance.objects.filter(lieu=lieu, projection__film__titre=film)
            if date and film and not lieu:  # 2
                seances = Seance.objects.filter(date=date, projection__film__titre=film)
            if date and not film and not lieu:
                seances = Seance.objects.filter(date=date)
            if film and not date and not lieu:
                seances = Seance.objects.filter(projection__film__titre=film)
            if lieu and not film and not date:
                seances = Seance.objects.filter(lieu=lieu)
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
    elif int(value) == 7:
        catalogues = Catalogue.objects.all()
        context = {
            'catalogues' : catalogues
        }
        return render(request, 'seances/content/catalogues.html', context)
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