from django.conf.urls import url

from . import views # import views so we can use them in urls.

urlpatterns = [
    url(r'^$', views.listing, name='listing'),
    url(r'^populated(?P<populated>[0-9]+)(?P<seance_id>[0-9]+)/$', views.listing, name='listing2'),
    url(r'^(?P<film_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^content/(?P<value>\d+)/$', views.content, name='content'),
    # url(r'^?Lieu=(?P<value_lieu>\d+)&Date=(?P<value_lieu>\d+)&Film=&query=Valider$', views.populated_listing, name='populated_listing'),
]