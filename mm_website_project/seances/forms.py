from django import forms
from .models import Film, Seance, Projection

class FormSeances(forms.Form):  #  this form is used to filter the seances on the
    #   appropriate page.
    location_dict = []
    date_dict = []
    film_dict = []
    for seance in Seance.objects.all():
        if (seance.lieu, seance.lieu) not in location_dict:
            location_dict.append((seance.lieu, seance.lieu))
        if (seance.date, seance.date) not in date_dict:
            date_dict.append((seance.date, seance.date))
    for film in Film.objects.all():
        if (film.titre, film.titre) not in film_dict:
            film_dict.append((film.titre, film.titre))
    location_dict.sort()
    date_dict.sort()
    film_dict.sort()
    Lieu = forms.MultipleChoiceField(choices=location_dict, required=False)
    Date = forms.MultipleChoiceField(choices=date_dict, required=False)
    Film = forms.MultipleChoiceField(choices=film_dict, required=False)