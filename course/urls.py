from django.contrib import admin
from django.urls import path, include

from . import views as course_views

urlpatterns = [
    path('<slug:id>', course_views.coursePage, name='course-page'),
    path('participants/<slug:id>', course_views.Participants, name='course-participants'),
    path('newdoc/<slug:id>', course_views.createDocument, name='create-document'),
    path('newlink/<slug:id>', course_views.createLink, name='create-link')
]