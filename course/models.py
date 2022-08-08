from django.utils import timezone
from django.db import models
from users.models import CustomUser
import statistics, os, uuid, math
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

    def visible_assignment_list(self):
        """ Returns LIST of all the Assignment objects accessible to everyone in the course """
        lst=[]
        for sec in self.coursesection_set.filter(show_on_main_page=True):
            for i in sec.item_set.all():
                if i.related_object_type()=='assignment' and i.access==3:
                    lst.append(i.related_object())
        return lst
    
    def visible_submission_list(self, student):
        return [Submission.objects.get(assignment=a, submitter=student) for a in self.visible_assignment_list()]
    
    def student_grade_total(self, student):
        try:
            return round(sum([s.grade or 0 for s in self.visible_submission_list(student)]),3)
        except statistics.StatisticsError:
            return '-'
    
    def course_grade_total(self):
        try:
            return round(sum([s.max_grade or 0 for s in self.visible_assignment_list()]),3)
        except statistics.StatisticsError:
            return '-'

    def grade_avg(self):
        try:
            return round(statistics.mean([self.student_grade_total(stu) for stu in self.students.all()]),3)
        except statistics.StatisticsError:
            return '-'

    def grade_stdev(self):
        try:
            return round(statistics.stdev([self.student_grade_total(stu) for stu in self.students.all()]),3)
        except statistics.StatisticsError:
            return '-'
    
    def save(self, *args, **kwargs):
        if self._state.adding == True:
            super().save(*args, **kwargs)
            m = CourseSection(title='Materials', course=self)
            m.save()
        return super().save(*args, **kwargs)

class CourseSection(models.Model):
    class AccessChoices(models.IntegerChoices):
        author_only = 1
        teachers_only = 2
        everyone = 3
    title = models.CharField(max_length=200)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    access = models.PositiveSmallIntegerField(choices=AccessChoices.choices, default=2)
    show_on_main_page = models.BooleanField(default=True)

    def __str__(self):
        return str(self.course)+': '+self.title



@cleanup.ignore
class Item(models.Model):

    class AccessChoices(models.IntegerChoices):
        author_only = 1
        teachers_only = 2
        everyone = 3

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

    def related_object(self):
        try:
            return self.document
        except:
            try:
                return self.link
            except:
                try:
                    return self.text
                except:
                    try:
                        return self.page
                    except:
                        return self.assignment
    
    def related_object_type(self):
        try:
            self.document
            return 'document'
        except:
            try:
                self.link
                return 'link'
            except:
                try:
                    self.text
                    return 'text'
                except:
                    try:
                        self.page
                        return 'page'
                    except:
                        self.assignment
                        return 'assignment'



class Document(models.Model):

    def material_upload(instance, filename):
        return os.path.join('course', str(instance.item.section.course.id), filename)

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
        self.item.icon=os.path.join(settings.MEDIA_ROOT, 'course/icons', icon_list.get(ext, 'default.jpg'))
        if self.item.display_text=='':
            self.item.display_text=self.file.name.split('/')[-1].split('.')[0]
        self.item.url=self.file.url
        self.item.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.item.display_text


class Link(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.item.icon=os.path.join(settings.MEDIA_ROOT,'course/icons/url.jpg')
        if self._state.adding and self.item.display_text=='':
            self.item.display_text=self.url
        self.item.url=self.url
        self.item.save()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.url


class Text(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        n=50
        s=self.content
        if len(s)<=n:
            return s
        else:
            return s[:n]+'...'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.item.display_text=str(self)
        self.item.save()
        return super().save(*args, **kwargs)


class Page(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    section = models.OneToOneField(CourseSection, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.section.show_on_main_page = False
        self.section.save()
        self.item.icon = os.path.join(settings.MEDIA_ROOT,'course/icons/page.jpg')
        if self.item.display_text == '':
            self.item.display_text = self.section.title
        self.item.save()
        super().save(*args, **kwargs)
        self.item.url = 'page/'+str(self.id)
        self.item.save()
        return super().save(*args, **kwargs)



class Assignment(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    section = models.OneToOneField(CourseSection, on_delete=models.CASCADE)
    # release_time = models.DateTimeField(default=timezone.now)
    due_time = models.DateTimeField()
    late_due_time = models.DateTimeField(blank=True, null=True)
    max_grade = models.FloatField(default=100.0)

    def save(self, *args, **kwargs):
        is_new=self._state.adding
        self.section.show_on_main_page = False
        self.section.save()
        self.item.icon = os.path.join(settings.MEDIA_ROOT,'course/icons/assignment.png')
        if self.item.display_text == '':
            self.item.display_text = self.section.title
        self.section.title = self.item.display_text
        self.section.save()
        self.item.save()
        if self.late_due_time=='':
            self.late_due_time=self.due_time
        super().save(*args, **kwargs)
        self.item.url = 'assignment/'+str(self.id)
        self.item.save()
        if is_new:
            for st in self.section.course.students.all():
                sub = Submission(assignment=self, submitter=st)
                sub.save()
        return super().save(*args, **kwargs)
    
    def release(self):
        self.item.access = 3
        self.item.save()
        self.section.access = 3
        self.section.save()
        for i in self.section.item_set.all():
            i.access = 3
            i.save()
        self.save()
    
    def grade_avg(self):
        try:
            return round(statistics.fmean([s.grade for s in self.submission_set.filter(status=3)]),3)
        except statistics.StatisticsError:
            return None

    def grade_stdev(self):
        try:
            return round(statistics.stdev([s.grade for s in self.submission_set.filter(status=3)]),3)
        except statistics.StatisticsError:
            return None



class Submission(models.Model):

    class StatusChoices(models.IntegerChoices):
        no_submission = 1, 'No Submission'
        ungraded = 2, 'Ungraded'
        graded = 3, 'Graded'

    def submission_upload(instance, filename):
        name=filename.split('.')[0]
        ext=filename.split('.')[-1]
        return os.path.join('course', str(instance.assignment.item.section.course.id), str(instance.submitter.kerberos), name+'-'+str(uuid.uuid4())+'.'+ext)

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submitter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to=submission_upload, blank=True, null=True, max_length=500)
    submitted_file_name = models.CharField(max_length=200, blank=True)
    submitted_file_icon = models.ImageField(blank=True, null=True)
    submitting_time = models.DateTimeField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=StatusChoices.choices, default=1)
    grade = models.FloatField(blank=True, null=True)
    grader = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 2},
        blank=True,
        null=True,
        related_name='submissions_graded'
    )
    grader_comments = models.TextField(blank=True)
    grading_time = models.DateTimeField(blank=True, null=True)

    def submit(self, file, name):
        self.submitted_file=file
        if name=='':
            self.submitted_file_name=file.name.split('/')[-1].split('.')[0]
        else:
            self.submitted_file_name=name
        ext=file.name.split('.')[-1]
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
        self.submitted_file_icon=os.path.join(settings.MEDIA_ROOT, 'course/icons', icon_list.get(ext, 'default.jpg'))
        self.status = 2
        self.submitting_time = timezone.now()
        self.save()
