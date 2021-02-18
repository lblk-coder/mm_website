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
    annee = models.SmallIntegerField(null=True)
    duree = models.SmallIntegerField(null=True)
    synopsis = models.TextField(max_length=10000, blank=True, default='')
    picture = models.CharField(max_length=500, blank=True, default='')
    page_allocine = models.URLField(blank=True, default='')

    def __str__(self):
        return self.titre

class Projection(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    heure = models.TimeField()
    animation = models.TextField(max_length=10000, blank=True, default='')
    tarif = models.SmallIntegerField(null=True)

    def __str__(self):
        msg = "Projection de "+str(self.film)+" à "+str(self.seance.lieu)+" le "+str(self.seance.date)+" à "+str(self.heure)
        return self.titre
