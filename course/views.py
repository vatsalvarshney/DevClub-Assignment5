from django.shortcuts import render,redirect
from .models import Course
from users.models import Role
from django.contrib.auth.decorators import login_required


def dashboardRedirect(request):
    return redirect('dashboard')

@login_required(login_url='login')
def dashboard(request):
    rl=request.user.role.all()
    context = {
        'isstudent': rl.contains(Role.objects.get(id=3)),
        'isinstructor': rl.contains(Role.objects.get(id=2)),
        'isadmin': rl.contains(Role.objects.get(id=1))
    }
    return render(request, 'course/dashboard.html', context)


def context(request, id):
    course=Course.objects.get(id=id)
    context= {
        'course': course,
        'enrolled': request.user.courses_studying.contains(course) or request.user.courses_teaching.contains(course) or request.user.courses_coordinating.contains(course)
    }
    return context

@login_required(login_url='login')
def coursePage(request, id):
    return render(request, 'course/course-page.html', context(request, id))

@login_required(login_url='login')
def courseInfo(request, id):
    return render(request, 'course/course-info.html', context(request, id))