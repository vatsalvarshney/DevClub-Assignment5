import datetime
from dateutil import parser
from django.shortcuts import render,redirect
from .forms import *
from users.models import Role, CustomUser
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages


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
            messages.success(request, 'Course has been updated!')
            return redirect(reverse('course-home', args=[id]))
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
            messages.success(request, f'Section "{sec.title}" has been created!')
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
            messages.success(request, f'{item.related_object_type().capitalize()} "{item.display_text}" has been created!')
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
            messages.success(request, f'Page "{sec.title}" has been created!')
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
            messages.success(request, f'Section "{sec.title}" has been updated!')
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
            messages.success(request, f'{item.related_object_type().capitalize()} "{item.display_text}" has been updated!')
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
        form = ConfirmationForm(request.POST)
        if form.is_valid and request.POST.get('agree'):
            t=item.display_text
            i=item.related_object_type().capitalize()
            item.delete()
            messages.success(request, f'{i} "{t}" has been deleted successfully')
            return redirect(reverse('course-home', args=[id]))
    else:
        form = ConfirmationForm()
    c['form']=form
    return render(request, 'course/delete-item.html', c)

def deleteSection(request, id, sec_id):
    c=context(request, id)
    sec=CourseSection.objects.get(id=sec_id)
    c['sec']=sec
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid and request.POST.get('agree'):
            t=sec.title
            sec.delete()
            messages.success(request, f'Section "{t}" has been deleted successfully')
            return redirect(reverse('course-home', args=[id]))
    else:
        form = ConfirmationForm()
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
            messages.success(request, f'Page "{sec.title}" has been created!')
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
            messages.success(request, f'{item.related_object_type().capitalize()} "{item.display_text}" has been created!')
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
            messages.success(request, f'{item.related_object_type().capitalize()} "{item.display_text}" has been updated!')
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
        form = ConfirmationForm(request.POST)
        if form.is_valid and request.POST.get('agree'):
            t=item.display_text
            i=item.related_object_type().capitalize()
            item.delete()
            messages.success(request, f'{i} "{t}" has been deleted successfully')
            return redirect(reverse('page', args=[id,page_id]))
    else:
        form = ConfirmationForm()
    c['form']=form
    return render(request, 'course/delete-item.html', c)


def createAssignment(request, id):
    c=context(request, id)
    if request.method == 'POST':
        aform = AssignmentCreationForm(request.POST)
        aform.fields['section'].queryset=CourseSection.objects.filter(course=c['course'], show_on_main_page=True)
        form = SectionCreationFormForPage(request.POST)
        if aform.is_valid() and form.is_valid():
            item=Item(
                author=request.user,
                section=aform.cleaned_data.get('section'),
                access=2,
                display_text=request.POST.get('title')
            )
            item.save()
            sec=CourseSection(
                title = request.POST.get('title'),
                course = c['course'],
                access = 2
            )
            sec.save()
            # l1=request.POST.get('due_time_0').split('-')
            # dt1=parser.parse(request.POST.get('due_time_0'))
            # tm1=parser.parse(request.POST.get('due_time_1'))
            # dt1=datetime.datetime(int(l1[0]),int(l1[1]),int(l1[2]))
            # tm1=datetime.datetime.strptime(request.POST.get('due_time_1')).time()
            asgmt=Assignment(
                item = item,
                section = sec,
                due_time = request.POST.get('due_time'),
                late_due_time = request.POST.get('late_due_time'),
                max_grade = request.POST.get('max_grade')
                # due_time = datetime.datetime.combine(dt1,tm1),
                # due_time = datetime.datetime.combine(dt1,tm1),
                # late_due_time = (request.POST.get('late_due_time_0'),request.POST.get('late_due_time_1')),
            )
            asgmt.save()
            messages.success(request, f'Assignment {sec.title} has been created!')
            return redirect(reverse('assignment', args=[id,asgmt.id]))
    else:
        aform = AssignmentCreationForm()
        aform.fields['section'].queryset=CourseSection.objects.filter(course=c['course'], show_on_main_page=True)
        form = SectionCreationFormForPage()
    c['iform']=aform
    c['form']=form
    c['item_type']='Assignment'
    return render(request, 'course/new-item.html', c)

def assignment(request, id, assignment_id):
    c=context(request, id)
    c['assignment']=Assignment.objects.get(id=assignment_id)
    c['sec']=c['assignment'].section
    c['sub_allowed']=c['assignment'].due_time>timezone.now()
    if c['isstudent']:
        c['submission']=Submission.objects.get(assignment=c['assignment'], submitter=request.user)
    c['ungraded_set']=Submission.objects.filter(assignment=c['assignment'], status=2)
    c['graded_set']=Submission.objects.filter(assignment=c['assignment'], status=3)
    c['no_submission_set']=Submission.objects.filter(assignment=c['assignment'], status=1)
    return render(request, 'course/assignment.html', c)

def releaseAssignment(request, id, assignment_id):
    c=context(request, id)
    c['assignment']=Assignment.objects.get(id=assignment_id)
    c['sec']=c['assignment'].section
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            c['assignment'].release()
            messages.success(request, f'Assignment {c["sec"].title} has been released to students!')
            return redirect(reverse('assignment', args=[id,assignment_id]))
    else:
        form = ConfirmationForm()
    c['form']=form
    return render(request, 'course/release-assignment.html', c)


def updateAssignment(request, id, assignment_id):
    c=context(request, id)
    asgmt=Assignment.objects.get(id=assignment_id)
    item=asgmt.item
    if request.method == 'POST':
        iform = ItemCreationForm(request.POST, instance=item)
        iform.fields['display_text'].label='title'
        iform.fields['section'].queryset=CourseSection.objects.filter(course=c['course'], show_on_main_page=True)
        aform = AssignmentUpdateForm(request.POST, instance=asgmt)
        if iform.is_valid() and aform.is_valid():
            item.save()
            asgmt.save()
            messages.success(request, f'Assignment {asgmt.section.title} has been updated!')
            return redirect(reverse('assignment', args=[id,assignment_id]))
    else:
        iform = ItemCreationForm(instance=item)
        iform.fields['section'].queryset=CourseSection.objects.filter(course=c['course'], show_on_main_page=True)
        iform.fields['display_text'].label='Title'
        aform = AssignmentUpdateForm(instance=asgmt)
    c['iform']=iform
    c['form']=aform
    c['item_type']='Assignment'
    c['assignment']=asgmt
    return render(request, 'course/update-item.html', c)


def createAssignmentItem(request, id, assignment_id, model, modelform, modelfields, excludedfields=[]):
    c=context(request,id)
    if request.method == 'POST':
        iform = ItemCreationForm(request.POST)
        iform.fields['section'].widget = forms.HiddenInput()
        iform.fields['section'].required = False
        form = modelform(request.POST, request.FILES)
        if iform.is_valid():
            item=Item(
                author=request.user,
                section=Assignment.objects.get(id=assignment_id).section,
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
            messages.success(request, f'{item.related_object_type().capitalize()} "{item.display_text}" has been created!')
            return redirect(reverse('assignment', args=[id, assignment_id]))
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

def createAssignmentLink(request, id, assignment_id):
    return createAssignmentItem(request, id, assignment_id, Link, LinkCreationForm, ['url'])

def createAssignmentDocument(request, id, assignment_id):
    return createAssignmentItem(request, id, assignment_id, Document, DocumentCreationForm, ['file'])

def createAssignmentText(request, id, assignment_id):
    return createAssignmentItem(request, id, assignment_id, Text, TextCreationForm, ['content'], ['display_text'])


def updateAssignmentItem(request, id, assignment_id, ins_id, model, modelform, modelfields, excludedfields=[]):
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
            messages.success(request, f'{item.related_object_type().capitalize()} "{item.display_text}" has been updated!')
            return redirect(reverse('assignment', args=[id,assignment_id]))
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

def updateAssignmentDocument(request, id, assignment_id, document_id):
    return updateAssignmentItem(request, id, assignment_id, document_id, Document, DocumentCreationForm, ['file'])

def updateAssignmentLink(request, id, assignment_id, link_id):
    return updateAssignmentItem(request, id, assignment_id, link_id, Link, LinkCreationForm, ['url'])

def updateAssignmentText(request, id, assignment_id, text_id):
    return updateAssignmentItem(request, id, assignment_id, text_id, Text, TextCreationForm, ['content'], ['display_text'])

def deleteAssignmentItem(request, id, assignment_id, item_id):
    c=context(request, id)
    item=Item.objects.get(id=item_id)
    c['item']=item
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid and request.POST.get('agree'):
            t=item.display_text
            i=item.related_object_type().capitalize()
            item.delete()
            messages.success(request, f'{i} "{t}" has been deleted successfully')
            return redirect(reverse('assignment', args=[id,assignment_id]))
    else:
        form = ConfirmationForm()
    c['form']=form
    return render(request, 'course/delete-item.html', c)


def makeSubmission(request, id, assignment_id):
    c=context(request,id)
    assignment = Assignment.objects.get(id=assignment_id)
    submission = Submission.objects.get(assignment=assignment, submitter=request.user)
    if request.method == 'POST':
        form = MakeSubmissionForm(request.FILES, request.POST, instance=submission)
        if form.is_valid():
            submission.submit(request.FILES.get('submitted_file'), request.POST.get('submitted_file_name'))
            messages.success(request, 'Assignment has been submitted successfully!')
            return redirect(reverse('assignment', args=[id, assignment_id]))
    else:
        form = MakeSubmissionForm(instance=submission)
    form.fields['submitted_file'].label = 'Submission File'
    form.fields['submitted_file_name'].label = 'Display File Name'
    c['form']=form
    c['submission']=submission
    c['assignment']=assignment
    c['sec']=c['assignment'].section
    c['sub_allowed']=assignment.due_time>timezone.now()
    return render(request, 'course/make-submission.html', c)


def viewStudentSubmission(request, id, assignment_id, submission_id):
    c=context(request, id)
    c['submission']=Submission.objects.get(id=submission_id)
    c['assignment']=c['submission'].assignment
    c['sec']=c['assignment'].section
    return render(request, 'course/view-student-submission.html', c)

def markGrade(request, id, assignment_id, submission_id):
    c=context(request, id)
    c['submission']=Submission.objects.get(id=submission_id)
    c['assignment']=c['submission'].assignment
    c['sec']=c['assignment'].section
    if request.method == 'POST':
        form = MarkGradeForm(request.POST, instance=c['submission'])
        if form.is_valid():
            c['submission'].grading_time=timezone.now()
            c['submission'].grader=request.user
            c['submission'].status=3
            c['submission'].save()
            return redirect(reverse('view-student-submission', args=[id, assignment_id, submission_id]))
    else:
        form = MarkGradeForm(instance=c['submission'])
    c['form']=form
    return render(request, 'course/mark-grade.html', c)


def grades(request, id):
    c=context(request,id)
    if c['isstudent']:
        return redirect(reverse('student-grades', args=[id,request.user.kerberos]))
    g_list=[]
    for stu in c['course'].students.all():
        g_list.append((stu,c['course'].student_grade_total(stu)))
    c['g_list']=g_list
    return render(request, 'course/grades.html', c)

def studentGrades(request, id, k):
    c=context(request,id)
    stu=CustomUser.objects.get(kerberos=k)
    c['allowed']=(request.user==stu or c['isinstructor'])
    c['sub_list']=c['course'].visible_submission_list(stu)
    c['student_grade_total']=c['course'].student_grade_total(stu)
    return render(request, 'course/student-grades.html', c)