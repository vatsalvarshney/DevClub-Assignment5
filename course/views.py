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

# @login_required(login_url='login')
# def createItem(request, id):
#     if request.method == 'POST':
#         form = ItemCreationForm(request.POST)
#         if form.is_valid():
#             item=Item(
#                 author=request.user,
#                 section=form.cleaned_data.get('section'),
#                 access=form.cleaned_data.get('access'),
#                 display_text=form.cleaned_data.get('display_text')
#             )
#             # item=form.save()
#             # item.update(author=request.user)
#             item.save()
#             return createDocument(request, id, item)
#     else:
#         form=ItemCreationForm()
#     return render(request, 'course/newitem.html', {'form': form})


@login_required(login_url='login')
def createDocument(request, id):
    c=context(request,id)
    if request.method == 'POST':
        iform = ItemCreationForm(request.POST)
        form = DocumentCreationForm(request.FILES)
        # if iform.is_valid() and form.is_valid():
        if iform.is_valid():
            item=Item(
                author=request.user,
                section=iform.cleaned_data.get('section'),
                access=iform.cleaned_data.get('access'),
                display_text=iform.cleaned_data.get('display_text')
            )
            item.save()
            doc=Document(
                file=request.FILES['file'],
                item=item
            )
            doc.item=item
            doc.save()
            item.url=doc.file.url
            item.save()
            return redirect(f'../{id}')
    else:
        iform=ItemCreationForm()
        form=DocumentCreationForm()
    c['iform']=iform
    c['form']=form
    return render(request, 'course/newitem.html', c)
    # return render(request, 'course/newitem.html', {'iform': iform, 'form': form})

