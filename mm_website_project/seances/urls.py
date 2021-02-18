from django.conf.urls import url

from . import views # import views so we can use them in urls.

urlpatterns = [
    url(r'^$', views.listing, name='listing'),
    url(r'^(?P<film_id>[0-9]+)/$', views.detail, name='detail'),
]