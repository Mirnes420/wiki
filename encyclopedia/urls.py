from django.urls import path
from encyclopedia import util
from encyclopedia import util, views
from django.conf.urls import url


urlpatterns = [
    path("", views.index, name="index"),
    path("<title>", views.get_by_title, name="title_name"), 
    url(r'^random/title', views.random_entry, name="random"),
    path("create/", views.create_entry, name="create"),
    path("edit/", views.edit_entry, name="edit"),
    path("delete/", views.delete_entry, name="delete"),
    path("save/", util.save_entry, name="save"),
    url(r'^/', views.search, name = 'search')
]
