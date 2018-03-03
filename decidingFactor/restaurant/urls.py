from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', auth_views.login),
    url(r'^signup/$', views.signup),
    url(r'^restaurant/$', views.restaurant),
]
