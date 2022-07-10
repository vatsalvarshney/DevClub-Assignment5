from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


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


class CustomUser(AbstractBaseUser, PermissionsMixin):
    kerberos        = models.CharField(max_length=9, unique=True)
    first_name      = models.CharField(max_length=100)
    middle_name     = models.CharField(max_length=100, blank=True)
    last_name       = models.CharField(max_length=100, blank=True)
    department      = models.CharField(max_length=100)
    email           = models.EmailField(max_length=100)
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
        return self.first_name+' '+self.middle_name+' '+self.last_name

