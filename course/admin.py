from django.contrib import admin

from .models import Course, CourseSection, Grade

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'semester', 'coordinator')


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'access')


# admin.site.register(Material)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade', 'student', 'course')
