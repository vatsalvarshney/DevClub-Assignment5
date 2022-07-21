from django.urls import path

from . import views as course_views

urlpatterns = [
    path('', course_views.courseHome, name='course-home'),
    path('participants/', course_views.courseParticipants, name='course-participants'),

    path('new/section/', course_views.createSection, name='create-section'),
    path('new/document/', course_views.createDocument, name='create-document'),
    path('new/link/', course_views.createLink, name='create-link'),
    path('new/text/', course_views.createText, name='create-text'),
    path('new/page/', course_views.createPage, name='create-page'),

    path('update/course/', course_views.updateCourse, name='update-course'),
    path('update/section/<int:sec_id>', course_views.updateSection, name='update-section'),
    path('update/document/<int:document_id>', course_views.updateDocument, name='update-document'),
    path('update/link/<int:link_id>', course_views.updateLink, name='update-link'),
    path('update/text/<int:text_id>', course_views.updateText, name='update-text'),
    path('update/page/<int:page_id>', course_views.updatePage, name='update-page'),

    path('delete/section/<int:sec_id>', course_views.deleteSection, name='delete-section'),
    path('delete/item/<int:item_id>', course_views.deleteItem, name='delete-item'),

    path('page/<int:page_id>/', course_views.page, name='page'),
    path('page/<int:page_id>/new/document/', course_views.createPageDocument, name='create-page-document'),
    path('page/<int:page_id>/new/link/', course_views.createPageLink, name='create-page-link'),
    path('page/<int:page_id>/new/text/', course_views.createPageText, name='create-page-text'),
    path('page/<int:page_id>/update/document/<int:document_id>', course_views.updatePageDocument, name='update-page-document'),
    path('page/<int:page_id>/update/link/<int:link_id>', course_views.updatePageLink, name='update-page-link'),
    path('page/<int:page_id>/update/text/<int:text_id>', course_views.updatePageText, name='update-page-text'),
    path('page/<int:page_id>/delete/item/<int:item_id>', course_views.deletePageItem, name='delete-page-item'),

]