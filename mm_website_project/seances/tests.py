from django.test import TestCase
from django.urls import reverse
from .models import Seance, Film, Projection, CarouselSlider
import datetime
import pytz
from io import BytesIO

# home page test
class HomePageTestCase(TestCase):
    def setUp(self):
        film1 = Film.objects.create(titre="Life of Brian")
        #  creates a seance for 'tomorrow' based on datetime.date.today() method
        seance1 = Seance.objects.create(date=datetime.date.today()+datetime.timedelta(days=1))
        #  creates a projection with timezone infos set on Europe/Paris (= UTC+2)
        projection1 = Projection.objects.create(
            film=film1,
            seance=seance1,
            heure=datetime.time(13, 00, 00, tzinfo=pytz.timezone('Europe/Paris'))
        )

    # tests if home page returns 200
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    # tests if a seance exists on home page's context after being created
    def test_home_page_seance_is_in_context(self):
        response = self.client.get(reverse('home'))
        self.assertIsNotNone(response.context['seances'])

    # tests if a page_obj exists on home page's context when a seance exists
    def test_home_page_page_obj_is_in_context(self):
        response = self.client.get(reverse('home'))
        self.assertIsNotNone(response.context['page_obj'])

