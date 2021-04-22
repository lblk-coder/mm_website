from django.db import models

class Seance(models.Model):
    date = models.DateField()
    lieu = models.CharField(max_length=200, blank=True, default='')
    animations = models.TextField(max_length=10000, blank=True, default='')
    plein_air = models.BooleanField(default=False)
    festival = models.BooleanField(default=False)
    mois_du_doc = models.BooleanField(default=False)

    def __str__(self):
        msg = "Séance du "+str(self.date)+" ayant lieu à "+str(self.lieu)
        return msg

class Film(models.Model):
    titre = models.CharField(max_length=200, unique=True)
    real = models.CharField(max_length=200, blank=True, default='')
    acteurs = models.CharField(max_length=200, blank=True, default='')
    genre = models.CharField(max_length=200, blank=True, default='')
    annee = models.SmallIntegerField(blank=True, null=True)
    duree = models.SmallIntegerField(blank=True, null=True)
    pays = models.CharField(max_length=200, default='')
    age = models.SmallIntegerField(blank=True, null=True)
    synopsis = models.TextField(max_length=10000, blank=True, default='')
    photo = models.ImageField(blank=True, null=True)
    page_allocine = models.URLField(blank=True, default='')

    def __str__(self):
        return self.titre

class Projection(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    heure = models.TimeField()
    animation = models.TextField(max_length=10000, blank=True, default='')
    tarif = models.FloatField(blank=True, null=True)

    def __str__(self):
        msg = "Projection de "+str(self.film)+" à "+str(self.seance.lieu)+" le "+str(self.seance.date)+" à "+str(self.heure)
        return msg

class CarouselSlider(models.Model):
    image = models.ImageField(blank=True, null=True)  # the pic used as slider

#    def __str__(self):
#        return self.titre

#    def save(self, *args, **kwars):  # changing the save method so there can only be one
        # Catalogue object with home_page == True (so only one Catalogue will be presented
        # on the home page)
#        if self.home_page == True:
#            try:
#                temp = Catalogue.objects.get(home_page=True)
#                if self != temp:
#                    temp.home_page = False
#                    temp.save()
#            except Catalogue.DoesNotExist:
#                pass
#            super(Catalogue, self).save(*args, **kwars)
#        else:
#            super(Catalogue, self).save(*args, **kwars)