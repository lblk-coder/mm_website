from django.shortcuts import render, get_object_or_404, redirect
import datetime
import pytz
from django.core.paginator import Paginator
from .models import Film, Seance, Projection, CarouselSlider
from .forms import FormSeances

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