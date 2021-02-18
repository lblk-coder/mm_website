from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from seances import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^seances/', include(('seances.urls', 'seances'), namespace='seances')),
    url(r'^thelmaetlouise/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns