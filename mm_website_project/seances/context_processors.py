from seances.models import CarouselSlider

# Customed context processor to load
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