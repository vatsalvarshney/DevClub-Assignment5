from django import forms
from .models import Course, CourseSection, Item, Document, Link, Text, Page, Assignment, Submission, Grade
from django.forms.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminSplitDateTime

class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description')

class SectionCreationForm(forms.ModelForm):
    class Meta:
        model = CourseSection
        fields = ('title', 'access')

class SectionCreationFormForPage(forms.ModelForm):
    class Meta:
        model = CourseSection
        fields = ('title',)

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

class ConfirmationForm(forms.Form):
    agree = forms.BooleanField(label='I Agree')

class AssignmentCreationForm(forms.ModelForm):
    # due_time = forms.SplitDateTimeField(widget=AdminSplitDateTime)
    # late_due_time = forms.SplitDateTimeField(widget=AdminSplitDateTime, required=False)
    class Meta:
        model = Assignment
        fields = ('section', 'due_time', 'late_due_time', 'max_grade')

class AssignmentUpdateForm(forms.ModelForm):
    # due_time = forms.SplitDateTimeField(widget=AdminSplitDateTime)
    # late_due_time = forms.SplitDateTimeField(widget=AdminSplitDateTime, required=False)
    class Meta:
        model = Assignment
        fields = ('due_time', 'late_due_time', 'max_grade')

class MakeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('submitted_file','submitted_file_name')

class MarkGradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('grade', 'grader_comments')