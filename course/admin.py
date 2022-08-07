from django.contrib import admin

from .models import Course, CourseSection, Item, Document, Link, Text, Page, Assignment, Submission

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'semester', 'coordinator')


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'access')


admin.site.register(Document)
admin.site.register(Link)
admin.site.register(Text)
admin.site.register(Page)
admin.site.register(Assignment)
admin.site.register(Submission)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    readonly_fields= ('time_posted', 'time_last_modified')
