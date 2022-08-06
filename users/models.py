from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
import os
from django.conf import settings



class Role(models.Model):
    admin = 1
    instructor = 2
    student = 3
    role_choices = (
        (admin, 'Admin'),
        (instructor, 'Instructor'),
        (student, 'Student')
    )
    
    id=models.PositiveSmallIntegerField(choices=role_choices,primary_key=True)

    def __str__(self):
        return self.get_id_display()


class CustomUserManager(BaseUserManager):

    def create_user(self, kerberos, first_name, department, email, password=None):
        if not kerberos:
            raise ValueError('Users must have a kerberos ID')
        user=self.model(
            kerberos=kerberos,
            first_name=first_name,
            department=department,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, kerberos, first_name, email, password=None):
        if not kerberos:
            raise ValueError('Users must have a kerberos ID')
        user=self.model(
            kerberos=kerberos,
            first_name=first_name,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.department='Admin'
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        for r in Role.objects.all():
            user.role.add(r)
        user.save()
        return user


def pfpUpload(instance, filename):
    new_path=os.path.join('users/profile-pics', instance.kerberos+'.'+filename.split('.')[-1])
    full_path=os.path.join(settings.MEDIA_ROOT,new_path)
    if os.path.exists(full_path):
        os.remove(full_path)
    return new_path

class CustomUser(AbstractBaseUser, PermissionsMixin):
    kerberos        = models.CharField(max_length=9, unique=True)
    first_name      = models.CharField(max_length=100)
    middle_name     = models.CharField(max_length=100, blank=True)
    last_name       = models.CharField(max_length=100, blank=True)
    department      = models.CharField(max_length=100)
    email           = models.EmailField(max_length=100)
    profile_pic     = models.ImageField(upload_to=pfpUpload, default='users/default-pfp.jpg')
    role            = models.ManyToManyField(Role)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superuser    = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'kerberos'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','email']

    def __str__(self):
        return self.kerberos
    
    def name(self):
        if self.middle_name=='':
            return self.first_name+' '+self.last_name
        return self.first_name+' '+self.middle_name+' '+self.last_name

    def roles(self):
        return "; ".join([r.get_id_display() for r in self.role.all()])

