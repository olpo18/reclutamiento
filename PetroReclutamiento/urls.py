"""PetroReclutamiento URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler403, handler404, handler500
from django.contrib import admin
# STATICFILES
from django.conf import settings
from django.conf.urls.static import static
from usuarios import views as users_views
from maestros import views as maestros_views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^password_change/$', auth_views.password_change, name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^$', RedirectView.as_view(pattern_name='login', permanent=False)),
    url(r'^login/', users_views.login_view, name='login'),
    url(r'^logout/', users_views.logout_view),
    url(r'^admin/', admin.site.urls),
    url(r'^convocatorias/', include('convocatorias.urls')),
    url(r'^publico/', include('publico.urls')),
    url(r'^personas/', include('usuarios.urls')),
    url(r'^atenciones/', include('atenciones.urls')),
    url(r'^educativo/', include('educativo.urls')),
    url(r'^laboral/', include('laboral.urls')),
    url(r'^cursos/', include('cursos.urls')),
    url(r'^api/maestros/', include('maestros.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    # url(r'^.*$', RedirectView.as_view(pattern_name='login', permanent=False))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler403 = maestros_views.handler403
handler404 = maestros_views.handler404
handler500 = maestros_views.handler500