from django import forms
from django.shortcuts import render,redirect
from .models import Course, CourseSection, Item, Document, Link, Text, Grade
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
def courseParticipants(request, id):
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

class TextCreationForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('content',)


@login_required(login_url='login')
def createItem(request, id, model, modelform, modelfields, excludedfields=[]):
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
            for field in modelfields:
                if request.POST.get(field) == None:
                    setattr(ins, field, request.FILES.get(field))
                else:
                    setattr(ins, field, request.POST.get(field))
            ins.save()
            item.save()
            return redirect('../../')
    else:
        iform=ItemCreationForm()
        iform.fields['section'].queryset=CourseSection.objects.filter(course=Course.objects.get(id=id))
        for ef in excludedfields:
            iform.fields[ef].widget = forms.HiddenInput()
        form=modelform()
    c['iform']=iform
    c['form']=form
    c['item_type']=model.__name__
    return render(request, 'course/new-item.html', c)

def createLink(request, id):
    return createItem(request, id, Link, LinkCreationForm, ['url'])

def createDocument(request, id):
    return createItem(request, id, Document, DocumentCreationForm, ['file'])

def createText(request, id):
    return createItem(request, id, Text, TextCreationForm, ['content'], ['display_text'])

@login_required(login_url='login')
def updateItem(request, id, ins_id, model, modelform, modelfields, excludedfields=[]):
    c=context(request,id)
    ins=model.objects.get(id=ins_id)
    item=ins.item
    if request.method == 'POST':
        iform = ItemCreationForm(request.POST, instance=item)
        form = modelform(request.POST, request.FILES, instance=ins)
        if iform.is_valid():
            item.save()
            for field in modelfields:
                if request.POST.get(field) == None:
                    setattr(ins, field, request.FILES.get(field))
                else:
                    setattr(ins, field, request.POST.get(field))
            ins.save()
            return redirect('../../')
    else:
        iform=ItemCreationForm(instance=item)
        iform.fields['section'].queryset=CourseSection.objects.filter(course=Course.objects.get(id=id))
        for ef in excludedfields:
            iform.fields[ef].widget = forms.HiddenInput()
        form=modelform(instance=ins)
    c['iform']=iform
    c['form']=form
    c['item_type']=model.__name__
    return render(request, 'course/update-item.html', c)

def updateDocument(request, id, document_id):
    return updateItem(request, id, document_id, Document, DocumentCreationForm, ['file'])

def updateLink(request, id, link_id):
    return updateItem(request, id, link_id, Link, LinkCreationForm, ['url'])

def updateText(request, id, text_id):
    return updateItem(request, id, text_id, Text, TextCreationForm, ['content'], ['display_text'])


class DeleteConfirmationForm(forms.Form):
    agree = forms.BooleanField(label='I Agree')

def deleteItem(request, id, item_id):
    c=context(request, id)
    item=Item.objects.get(id=item_id)
    c['item']=item
    if request.method == 'POST':
        form = DeleteConfirmationForm(request.POST)
        if form.is_valid and request.POST.get('agree'):
            item.delete()
            return redirect('../')
    else:
        form = DeleteConfirmationForm()
    c['form']=form
    return render(request, 'course/delete-confirmation.html', c)
