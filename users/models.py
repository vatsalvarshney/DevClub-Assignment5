from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_student(self, kerberos, first_name, department, email, password=None):
        if not kerberos:
            raise ValueError('Users must have a kerberos ID')
        user=self.model(
            kerberos=kerberos,
            first_name=first_name,
            department=department,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_student=True
        user.save(using=self._db)
        return user

    def create_instructor(self, kerberos, first_name, department, email, password=None):
        if not kerberos:
            raise ValueError('Users must have a kerberos ID')
        user=self.model(
            kerberos=kerberos,
            first_name=first_name,
            department=department,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_instructor=True
        user.save(using=self._db)
        return user

    def create_superuser(self, kerberos, first_name, department, email, password=None):
        if not kerberos:
            raise ValueError('Users must have a kerberos ID')
        user=self.model(
            kerberos=kerberos,
            first_name=first_name,
            department=department,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    kerberos        = models.CharField(max_length=9, unique=True)
    first_name      = models.CharField(max_length=100)
    middle_name     = models.CharField(max_length=100, blank=True)
    last_name       = models.CharField(max_length=100, blank=True)
    department      = models.CharField(max_length=100)
    email           = models.EmailField(max_length=100)
    is_instructor   = models.BooleanField(default=False)
    is_student      = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superuser    = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'kerberos'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','department','email']

    def __str__(self):
        return self.kerberos


# class Student(models.Model):
#     student_kerberos_id = models.CharField(max_length=9, unique=True)
#     first_name = models.CharField(max_length=50)
#     middle_name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     department = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100)