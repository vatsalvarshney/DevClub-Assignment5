from django.contrib import admin

from .models import Course, CourseSection, Document, Grade

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'semester', 'coordinator')


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'access')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    def course(self):
        return str(self.section.course)
    list_display = ('title', 'section', 'author', 'access', 'file')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade', 'student', 'course')
