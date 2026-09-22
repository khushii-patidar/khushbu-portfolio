from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("resume/download/", views.resume_download, name="resume_download"),
    path("contact/", views.contact, name="contact"),
]
