from django.db import models
from users.models import CustomUser
import statistics, os, uuid
from django.conf import settings


class Course(models.Model):
    semester      = models.CharField(max_length=4, help_text='4 digit code. Last 2 digits of academic year followed by 2 digits of semester number. Eg- 2101')
    course_code   = models.CharField(max_length=6, help_text='Eg- APL100, MCP101')
    title         = models.CharField(max_length=100)
    description   = models.TextField(blank=True)
    coordinator = models.ForeignKey(
        CustomUser,
        related_name = 'courses_coordinating',
        on_delete = models.CASCADE,
        limit_choices_to = {'role': 2},
        blank = True
    )
    teachers = models.ManyToManyField(
        CustomUser,
        related_name = 'courses_teaching',
        limit_choices_to = {'role': 2},
        blank = True
    )
    students = models.ManyToManyField(
        CustomUser,
        related_name = 'courses_studying',
        limit_choices_to = {'role': 3},
        blank = True
    )

    def __str__(self):
        return f'{self.semester}-{self.course_code}'

    def grade_count(self):
        return self.grade_set.all().count()

    def grade_avg(self):
        return statistics.fmean([g.grade for g in self.grade_set.all()])

    def grade_stdev(self):
        return statistics.stdev([g.grade for g in self.grade_set.all()])
    
    def save(self, *args, **kwargs):
        if self._state.adding == True:
            super().save(*args, **kwargs)
            ci = CourseSection(title='Course Information', course=self, access=3)
            m = CourseSection(title='Materials', course=self)
            ci.save()
            m.save()
        return super().save(*args, **kwargs)

class CourseSection(models.Model):
    class AccessChoices(models.IntegerChoices):
        teachers_only = 2
        everyone = 3
    title = models.CharField(max_length=256)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    access = models.PositiveSmallIntegerField(choices=AccessChoices.choices, default=2)

    def __str__(self):
        return str(self.course)+': '+self.title




class Document(models.Model):
    class AccessChoices(models.IntegerChoices):
        author_only = 1
        teachers_only = 2
        everyone = 3

    def material_upload(instance, filename):
        old_path=instance.file.path
        if os.path.exists(old_path):
            os.remove(old_path)
        return os.path.join(settings.MEDIA_ROOT, 'course', str(instance.section.course.id), '%s.%s' % (uuid.uuid4(), filename.split(".")[-1]))

    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE)
    file = models.FileField(upload_to=material_upload, max_length=500)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 2}
    )
    date_posted = models.DateTimeField()
    access = models.PositiveIntegerField(choices=AccessChoices.choices, default=1)
    title = models.CharField(max_length=256, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.title == '':
            self.title=self.file.name.split('/')[-1].split('.')[0]
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def url(self):
        return self.file.url
    


# class Post(models.Model):
#     class AccessChoices(models.IntegerChoices):
#         author_only = 1
#         teachers_only = 2
#         everyone = 3

#     section = models.ForeignKey(
#         CourseSection,
#         on_delete=models.CASCADE
#     )
#     author = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         limit_choices_to={'role': 2}
#     )
#     time_posted = models.DateTimeField(auto_now_add=True)
#     time_last_modified = models.DateTimeField(auto_now=True)
#     access = models.PositiveSmallIntegerField(choices=AccessChoices.choices, default=1)
#     title = models.CharField(max_length=256)




class Grade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    grade = models.FloatField()    

    def __str__(self):
        return str(self.grade)

    class Meta:
        ordering=('grade',)