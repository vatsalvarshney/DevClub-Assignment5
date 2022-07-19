from django.contrib import admin
from django.urls import path, include

from . import views as course_views

urlpatterns = [
    path('', course_views.coursePage, name='course-page'),
    path('participants/', course_views.courseParticipants, name='course-participants'),
    path('new/document/', course_views.createDocument, name='create-document'),
    path('new/link/', course_views.createLink, name='create-link'),
    path('new/text/', course_views.createText, name='create-text'),
    path('update/link/<int:link_id>', course_views.updateLink),
    path('update/text/<int:text_id>', course_views.updateText),
    path('update/document/<int:document_id>', course_views.updateDocument),
    path('delete/<int:item_id>', course_views.deleteItem)
    # path('page/<int:p>', course_views.page)
]