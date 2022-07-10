from django.contrib import admin
from django.urls import path, include

from . import views as course_views

urlpatterns = [
    path('<slug:id>', course_views.coursePage, name='course-page'),
    path('info/<slug:id>', course_views.courseInfo, name='course-info')
]