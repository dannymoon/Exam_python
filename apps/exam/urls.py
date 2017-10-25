from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.blank),
    url(r'^main$', views.index),
    url(r'^users/(?P<user_id>\d+)$', views.users),
    url(r'^quotes$', views.quotes),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^create$', views.create),
    url(r'^add_to_favorite$', views.add_to_favorite),
    url(r'^remove_from_favorite$', views.remove_from_favorite),

]