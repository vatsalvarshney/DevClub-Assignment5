from django import forms
from django.shortcuts import render,redirect
from .models import Course, CourseSection, Item, Document, Link, Grade
from users.models import Role, CustomUser
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
    isstudent=request.user.courses_studying.contains(course)
    isinstructor=request.user.courses_teaching.contains(course) or request.user.courses_coordinating.contains(course)
    context= {
        'course': course,
        'isstudent': isstudent,
        'isinstructor': isinstructor,
        'enrolled': isstudent or isinstructor
    }
    return context

@login_required(login_url='login')
def coursePage(request, id):
    return render(request, 'course/course-page.html', context(request, id))

@login_required(login_url='login')
def Participants(request, id):
    return render(request, 'course/course-participants.html', context(request, id))


class ItemCreationForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('section', 'access', 'display_text')

class DocumentCreationForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)

class LinkCreationForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('url',)


@login_required(login_url='login')
def createItem(request, id, model, modelform, modelfieldlist):
    c=context(request,id)
    if request.method == 'POST':
        iform = ItemCreationForm(request.POST)
        form = modelform(request.POST, request.FILES)
        if iform.is_valid():
            item=Item(
                author=request.user,
                section=iform.cleaned_data.get('section'),
                access=iform.cleaned_data.get('access'),
                display_text=iform.cleaned_data.get('display_text')
            )
            item.save()
            ins=model(item=item)
            for field in modelfieldlist:
                if request.POST.get(field) == None:
                    setattr(ins, field, request.FILES.get(field))
                else:
                    setattr(ins, field, request.POST.get(field))
            ins.save()
            item.save()
            return redirect(f'../{id}')
    else:
        iform=ItemCreationForm()
        form=modelform()
    c['iform']=iform
    c['form']=form
    return render(request, 'course/newitem.html', c)

def createLink(request, id):
    return createItem(request, id, Link, LinkCreationForm, ['url'])

def createDocument(request, id):
    return createItem(request, id, Document, DocumentCreationForm, ['file'])
