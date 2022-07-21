from django.shortcuts import render,redirect
from .forms import *
from users.models import Role, CustomUser
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def dashboardRedirect(request):
    return redirect(reverse('dashboard'))

@login_required(login_url='login')
def dashboard(request):
    rl=request.user.role.all()
    context = {
        'isstudent': rl.contains(Role.objects.get(id=3)),
        'isinstructor': rl.contains(Role.objects.get(id=2)),
        'isadmin': rl.contains(Role.objects.get(id=1))
    }
    return render(request, 'course/dashboard.html', context)

@login_required(login_url='login')
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

def courseHome(request, id):
    return render(request, 'course/course-home.html', context(request, id))

def courseParticipants(request, id):
    return render(request, 'course/course-participants.html', context(request, id))


def updateCourse(request, id):
    c=context(request, id)
    if request.method == 'POST':
        form = CourseUpdateForm(request.POST, instance=c['course'])
        if form.is_valid():
            c['course'].save()
            return redirect(reverse('course-home', args=[id]))
            # return redirect('../../')
    else:
        form =CourseUpdateForm(instance=c['course'])
    c['form']=form
    return render(request, 'course/update-course.html', c)


def createSection(request, id):
    c=context(request,id)
    if request.method == 'POST':
        form = SectionCreationForm(request.POST)
        if form.is_valid():
            sec=CourseSection(
                title = form.cleaned_data.get('title'),
                course = c['course'],
                access = form.cleaned_data.get('access')
            )
            sec.save()
            return redirect(reverse('course-home', args=[id]))
    else:
        form =SectionCreationForm()
    c['form']=form
    return render(request, 'course/new-section.html', c)


def createItem(request, id, model, modelform, modelfields, excludedfields=[]):
    c=context(request,id)
    if request.method == 'POST':
        iform = ItemCreationForm(request.POST)
        iform.fields['section'].queryset=CourseSection.objects.filter(course=c['course'], show_on_main_page=True)
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
            return redirect(reverse('course-home', args=[id]))
    else:
        iform=ItemCreationForm()
        iform.fields['section'].queryset=CourseSection.objects.filter(course=c['course'], show_on_main_page=True)
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


def createPage(request, id):
    c=context(request, id)
    if request.method == 'POST':
        iform = ItemCreationForm(request.POST)
        iform.fields['section'].queryset=CourseSection.objects.filter(course=c['course'], show_on_main_page=True)
        form = SectionCreationFormForPage(request.POST)
        if iform.is_valid() and form.is_valid():
            item=Item(
                author=request.user,
                section=iform.cleaned_data.get('section'),
                access=iform.cleaned_data.get('access'),
                display_text=iform.cleaned_data.get('display_text')
            )
            item.save()
            sec=CourseSection(
                title = request.POST.get('title'),
                course = c['course'],
                access = iform.cleaned_data.get('access')
            )
            sec.save()
            page=Page(
                item = item,
                section = sec
            )
            page.save()
            return redirect(reverse('page', args=[id,page.id]))
    else:
        iform = ItemCreationForm()
        iform.fields['section'].queryset=CourseSection.objects.filter(course=c['course'], show_on_main_page=True)
        form = SectionCreationFormForPage()
    c['iform']=iform
    c['form']=form
    c['item_type']='Page'
    return render(request, 'course/new-item.html', c)


def updateSection(request, id, sec_id):
    c=context(request, id)
    sec=CourseSection.objects.get(id=sec_id)
    if request.method == 'POST':
        form = SectionCreationForm(request.POST, instance=sec)
        if form.is_valid():
            sec.save()
            return redirect(reverse('course-home', args=[id]))
    else:
        form =SectionCreationForm(instance=sec)
    c['form']=form
    return render(request, 'course/update-section.html', c)


def updateItem(request, id, ins_id, model, modelform, modelfields, excludedfields=[]):
    c=context(request,id)
    ins=model.objects.get(id=ins_id)
    item=ins.item
    if request.method == 'POST':
        iform = ItemCreationForm(request.POST, instance=item)
        iform.fields['section'].queryset=CourseSection.objects.filter(course=c['course'], show_on_main_page=True)
        form = modelform(request.POST, request.FILES, instance=ins)
        if iform.is_valid():
            item.save()
            for field in modelfields:
                if request.POST.get(field) == None:
                    setattr(ins, field, request.FILES.get(field))
                else:
                    setattr(ins, field, request.POST.get(field))
            ins.save()
            return redirect(reverse('course-home', args=[id]))
    else:
        iform=ItemCreationForm(instance=item)
        iform.fields['section'].queryset=CourseSection.objects.filter(course=c['course'], show_on_main_page=True)
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


def deleteItem(request, id, item_id):
    c=context(request, id)
    item=Item.objects.get(id=item_id)
    c['item']=item
    if request.method == 'POST':
        form = DeleteConfirmationForm(request.POST)
        if form.is_valid and request.POST.get('agree'):
            item.delete()
            return redirect(reverse('course-home', args=[id]))
    else:
        form = DeleteConfirmationForm()
    c['form']=form
    return render(request, 'course/delete-item.html', c)

def deleteSection(request, id, sec_id):
    c=context(request, id)
    sec=CourseSection.objects.get(id=sec_id)
    c['sec']=sec
    if request.method == 'POST':
        form = DeleteConfirmationForm(request.POST)
        if form.is_valid and request.POST.get('agree'):
            sec.delete()
            return redirect(reverse('course-home', args=[id]))
    else:
        form = DeleteConfirmationForm()
    c['form']=form
    return render(request, 'course/delete-section.html', c)

def page(request, id, page_id):
    c=context(request, id)
    c['page']=Page.objects.get(id=page_id)
    c['sec']=c['page'].section
    return render(request, 'course/page.html', c)

def updatePage(request, id, page_id):
    c=context(request, id)
    page=Page.objects.get(id=page_id)
    item=page.item
    sec=page.section
    if request.method == 'POST':
        iform = ItemCreationForm(request.POST, instance=item)
        iform.fields['section'].queryset=CourseSection.objects.filter(course=c['course'], show_on_main_page=True)
        form = SectionCreationFormForPage(request.POST, instance=sec)
        if iform.is_valid() and form.is_valid():
            item.save()
            sec.save()
            page.save()
            return redirect(reverse('page', args=[id,page_id]))
    else:
        iform = ItemCreationForm(instance=item)
        iform.fields['section'].queryset=CourseSection.objects.filter(course=c['course'], show_on_main_page=True)
        form = SectionCreationFormForPage(instance=sec)
    c['iform']=iform
    c['form']=form
    c['item_type']='Page'
    c['page']=page
    return render(request, 'course/update-item.html', c)


def createPageItem(request, id, page_id, model, modelform, modelfields, excludedfields=[]):
    c=context(request,id)
    if request.method == 'POST':
        iform = ItemCreationForm(request.POST)
        iform.fields['section'].widget = forms.HiddenInput()
        iform.fields['section'].required = False
        form = modelform(request.POST, request.FILES)
        if iform.is_valid():
            item=Item(
                author=request.user,
                section=Page.objects.get(id=page_id).section,
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
            return redirect(reverse('page', args=[id, page_id]))
    else:
        iform=ItemCreationForm()
        iform.fields['section'].widget = forms.HiddenInput()
        iform.fields['section'].required = False
        for ef in excludedfields:
            iform.fields[ef].widget = forms.HiddenInput()
        form=modelform()
    c['iform']=iform
    c['form']=form
    c['item_type']=model.__name__
    return render(request, 'course/new-item.html', c)

def createPageLink(request, id, page_id):
    return createPageItem(request, id, page_id, Link, LinkCreationForm, ['url'])

def createPageDocument(request, id, page_id):
    return createPageItem(request, id, page_id, Document, DocumentCreationForm, ['file'])

def createPageText(request, id, page_id):
    return createPageItem(request, id, page_id, Text, TextCreationForm, ['content'], ['display_text'])


def updatePageItem(request, id, page_id, ins_id, model, modelform, modelfields, excludedfields=[]):
    c=context(request,id)
    ins=model.objects.get(id=ins_id)
    item=ins.item
    if request.method == 'POST':
        iform = ItemCreationForm(request.POST, instance=item)
        iform.fields['section'].widget = forms.HiddenInput()
        iform.fields['section'].required = False
        form = modelform(request.POST, request.FILES, instance=ins)
        if iform.is_valid():
            item.save()
            for field in modelfields:
                if request.POST.get(field) == None:
                    setattr(ins, field, request.FILES.get(field))
                else:
                    setattr(ins, field, request.POST.get(field))
            ins.save()
            return redirect(reverse('page', args=[id,page_id]))
    else:
        iform=ItemCreationForm(instance=item)
        iform.fields['section'].widget = forms.HiddenInput()
        iform.fields['section'].required = False
        for ef in excludedfields:
            iform.fields[ef].widget = forms.HiddenInput()
        form=modelform(instance=ins)
    c['iform']=iform
    c['form']=form
    c['item_type']=model.__name__
    return render(request, 'course/update-item.html', c)

def updatePageDocument(request, id, page_id, document_id):
    return updatePageItem(request, id, page_id, document_id, Document, DocumentCreationForm, ['file'])

def updatePageLink(request, id, page_id, link_id):
    return updatePageItem(request, id, page_id, link_id, Link, LinkCreationForm, ['url'])

def updatePageText(request, id, page_id, text_id):
    return updatePageItem(request, id, page_id, text_id, Text, TextCreationForm, ['content'], ['display_text'])

def deletePageItem(request, id, page_id, item_id):
    c=context(request, id)
    item=Item.objects.get(id=item_id)
    c['item']=item
    if request.method == 'POST':
        form = DeleteConfirmationForm(request.POST)
        if form.is_valid and request.POST.get('agree'):
            item.delete()
            return redirect(reverse('page', args=[id,page_id]))
    else:
        form = DeleteConfirmationForm()
    c['form']=form
    return render(request, 'course/delete-item.html', c)
