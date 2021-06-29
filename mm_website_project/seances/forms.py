from django import forms
from .models import Film, Seance, Projection

class FormSeances(forms.Form):  #  this form is used to filter the seances on the
    #   appropriate page.
    location_dict = [('','------')]  #the first tuple is the empty choice
    date_dict = [('','------')]
    film_dict = [('','------')]
    for seance in Seance.objects.all():
        if (seance.lieu, seance.lieu) not in location_dict:  # we don't wan't twice or more the same
            # lieu or date or film in the choices
            location_dict.append((seance.lieu, seance.lieu))
        if (seance.date, seance.date) not in date_dict:
            date_dict.append((seance.date, seance.date))
    for film in Film.objects.all():
        if (film.titre, film.titre) not in film_dict:
            if len(film.projection_set.all()) != 0:
                film_dict.append((film.titre, film.titre))
    location_dict.sort()
    try:  # 'try' is needed since empty date field raises a TypeError
        date_dict.sort()
    except:
        pass
    film_dict.sort()
    Lieu = forms.ChoiceField(choices=location_dict, required=False)
    Date = forms.ChoiceField(choices=date_dict, required=False)
    Film = forms.ChoiceField(choices=film_dict, required=False)

class NlForm(forms.Form):  # this form is used to register new emails to the newsletter
    email = forms.EmailField(required=True, label="Votre adresse mail")