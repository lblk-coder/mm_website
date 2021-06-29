from seances.models import CarouselSlider
from seances.forms import NlForm
from django.core.mail import send_mail

#  Customed context processor to load
#  on each page of the website the images of the carousel, uploaded by user.
def carousel(request):
    carousel_sliders_dict = {}
    for carousel_sliders in CarouselSlider.objects.all():
        if len(carousel_sliders_dict) == 0:
            carousel_sliders_dict[carousel_sliders] = True  # if True, it means it will
            # be the active slide
        else:
            carousel_sliders_dict[carousel_sliders] = False
    return { 'carousel_sliders_dict': carousel_sliders_dict }

def nlform(request):  #newsletter form
    if request.method == 'GET':
        nl_form = NlForm()
    else:
        nl_form = NlForm(request.POST)
        if nl_form.is_valid():
            email = nl_form.cleaned_data['email']
            send_mail(subject="Demande d'inscription à la newsletter",
                      from_email="loiclegros.eaclyon@gmail.com",
                      recipient_list=("loic.legros91@gmail.com",),
                      message="Demande d'ajout à la newsletter pour l'addresse : "+str(email))
            nl_form = NlForm()
    context = { 'nl_form': nl_form }
    return context