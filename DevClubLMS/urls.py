"""DevClubLMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from users import views as user_views
# from users.views import pfpChangeView
from course import views as course_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('register/student/', user_views.registerStudent, name='register-student'),
    path('register/instructor/', user_views.registerInstructor, name='register-instructor'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('user/<slug:k>', user_views.profile, name='profile'),
    path('user/pwdchange/', user_views.pwdChange, name='pwd-change'),
    path('user/pfpchange/', user_views.pfpChange, name='pfp-change'),
    path('', course_views.dashboardRedirect),
    path('dashboard/', course_views.dashboard, name='dashboard'),
    path('course/<int:id>/', include('course.urls'), name='course')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
