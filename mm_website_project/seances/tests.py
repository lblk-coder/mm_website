from django.test import TestCase
from django.urls import reverse
from .models import Seance, Film, Projection, CarouselSlider
import datetime
import pytz

def create_db_objects():
    film1 = Film.objects.create(titre="Life of Brian")
    #  creates a seance for 'tomorrow' based on datetime.date.today() method
    seance1 = Seance.objects.create(date=datetime.date.today() + datetime.timedelta(days=1), lieu="Flavin")
    #  creates a projection with timezone infos set on Europe/Paris (= UTC+2)
    projection1 = Projection.objects.create(
        film=film1,
        seance=seance1,
        heure=datetime.time(13, 00, 00, tzinfo=pytz.timezone('Europe/Paris'))
    )

# bdase objects creation tests

# tests home view
class HomePageTestCase(TestCase):
    def setUp(self):
        create_db_objects()

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

# tests the detail view
class DetailPageTestCase(TestCase):
    def setUp(self):
        create_db_objects()

    #tests if the view returns 200
    def test_detail_page(self):
        film_id = Film.objects.get(titre="Life of Brian").id
        response = self.client.get(reverse('seances:detail', args=(film_id,)))
        self.assertEqual(response.status_code, 200)

    #tests if the view returns 404
    def test_detail_page_returns_404(self):
        film_id = Film.objects.get(titre="Life of Brian").id+1
        response = self.client.get(reverse('seances:detail', args=(film_id,)))
        self.assertEqual(response.status_code, 404)

    # tests if a projection exists on detail page's context after being created
    def test_detail_page_projection_is_in_context(self):
        film_id = Film.objects.get(titre="Life of Brian").id
        response = self.client.get(reverse('seances:detail', args=(film_id,)))
        self.assertIsNotNone(response.context['projections'])

# tests if all the 'content' pages return 200
class ContentViewTestCase(TestCase):
    def test_content_view(self):
        for num in range(18):
            if num == 7:
                continue
            value = num
            response = self.client.get(reverse('seances:content', args=(value,)))
            self.assertEqual(response.status_code, 200)

# tests the listing view
class ListingPageTestCase(TestCase):
    def setUp(self):
        create_db_objects()

    # tests if the view returns 200
    def test_listing_page(self):
        response = self.client.get(reverse('seances:listing'))
        self.assertEqual(response.status_code, 200)

    # test if the view returns 200 if populated (the user clicked on a seance in the home page)
    def test_listing_page_populated(self):
        seance_id = Seance.objects.all()[0].id
        populated = 1
        response = self.client.get(reverse('seances:listing2', args=(populated, seance_id,)))
        self.assertEqual(response.status_code, 200)

# tests the context processors
#class ContextProcessorsTestCase(TestCase):
    #  tests if a carousel image appears on each page on the site
    #TODO def test_carousel(self):

