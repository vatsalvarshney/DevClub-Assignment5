from django.contrib import admin

from .models import Course, CourseSection, Item, Document, Link, Grade

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'semester', 'coordinator')


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'access')


admin.site.register(Document)
admin.site.register(Link)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    readonly_fields= ('time_posted', 'time_last_modified')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade', 'student', 'course')
