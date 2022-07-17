from django.db import models
from users.models import CustomUser
import statistics, os, uuid
from django.conf import settings
from django_cleanup import cleanup


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
    title = models.CharField(max_length=200)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    access = models.PositiveSmallIntegerField(choices=AccessChoices.choices, default=2)

    def __str__(self):
        return str(self.course)+': '+self.title



class AccessChoices(models.IntegerChoices):
    author_only = 1
    teachers_only = 2
    everyone = 3

@cleanup.ignore
class Item(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 2},
        blank=True
    )
    time_posted = models.DateTimeField(auto_now_add=True)
    time_last_modified = models.DateTimeField(auto_now=True)
    access = models.PositiveSmallIntegerField(choices=AccessChoices.choices, default=1)
    display_text = models.CharField(max_length=200, blank=True)
    icon = models.ImageField(default='course/icons/default.jpg')
    url = models.URLField(max_length=500,blank=True)


class Document(models.Model):

    def material_upload(instance, filename):
        # return os.path.join(settings.MEDIA_ROOT, 'course', str(instance.item.section.course.id), str(instance.item.section.id), '%s.%s' % (uuid.uuid4(), filename.split(".")[-1]))
        return os.path.join(settings.MEDIA_ROOT, 'course', str(instance.item.section.course.id), filename)

    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    file = models.FileField(upload_to=material_upload, max_length=500)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ext=self.file.name.split('.')[-1]
        icon_list={
            'pdf':'pdf.jpg',
            'txt':'txt.jpg',
            **dict.fromkeys(['jpg','jpeg','jfif','pjpeg','pjp','png','svg','webp'], 'image.jpg'),
            **dict.fromkeys(['doc','docx','docm','dot','dotx'], 'docx.jpg'),
            **dict.fromkeys(['ppt','pptx','pptm','pps','ppsx','ppsm','pot','potx','potm'], 'pptx.jpg'),
            **dict.fromkeys(['xls','xlsx','xlsm','xlt','xltx','xltm','xla','xlam','xll','xlm'], 'xlsx.jpg'),
            **dict.fromkeys(['zip','rar'], 'zip.jpg'),
            **dict.fromkeys(['m4a','mp3','wav','wma','aac','aa','aax','flac',], 'audio.jpg'),
            **dict.fromkeys(['mov','mp4','wmv','avi','flv','mkv'], 'video.jpg')
        }
        self.item.icon='/media/course/icons/' + icon_list.get(ext, 'default.jpg')
        if self._state.adding and self.item.display_text=='':
            self.item.display_text=self.file.name.split('/')[-1].split('.')[0]
        self.item.url=self.file.url
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.item.display_text


class Link(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.item.icon=os.path.join(settings.MEDIA_ROOT, 'course/icons/url.jpg')
        if self._state.adding and self.item.display_text=='':
            self.item.display_text=self.url
        self.item.url=self.url
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.url


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