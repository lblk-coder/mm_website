from django.shortcuts import render
from django.http import HttpResponse
from .models import Film, Seance, Projection

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