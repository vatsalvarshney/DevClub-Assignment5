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
admin.site.register(Item)
# class DocumentAdmin(admin.ModelAdmin):
#     def course(self):
#         return str(self.section.course)
#     list_display = ('display_text', 'file')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade', 'student', 'course')
