from django import forms
from .models import Course, CourseSection, Item, Document, Link, Text, Page, Grade

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

class DeleteConfirmationForm(forms.Form):
    agree = forms.BooleanField(label='I Agree')
