from django.db import models
from users.models import CustomUser


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


# class Grade(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)