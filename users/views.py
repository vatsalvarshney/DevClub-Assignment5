import os
from django.conf import settings
from django.shortcuts import render,redirect

from .admin import UserCreationForm
from .models import Role, CustomUser
from . import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import UpdateView
from django import forms
from django.contrib.messages.views import SuccessMessageMixin


def register(request):
    return render(request, 'users/preregister.html')

def registerStudent(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            r = Role.objects.get(id=3)
            form.save()
            kerberos=form.cleaned_data.get('kerberos')
            user=CustomUser.objects.get(kerberos=kerberos)
            user.role.add(r)
            user.save()
            messages.success(request, f'Your account has been created! Log in to continue')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def registerInstructor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            r = Role.objects.get(id=2)
            form.save()
            kerberos=form.cleaned_data.get('kerberos')
            user=CustomUser.objects.get(kerberos=kerberos)
            user.role.add(r)
            user.save()
            messages.success(request, f'Your account has been created! Log in to continue')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required(login_url='login')
def profile(request, k):
    if CustomUser.objects.filter(kerberos=k):
        view_user=CustomUser.objects.get(kerberos=k)
        if view_user.is_active:
            rl=view_user.role.all()
            context = {
                'isstudent': rl.contains(Role.objects.get(id=3)),
                'isinstructor': rl.contains(Role.objects.get(id=2)),
                'isadmin': rl.contains(Role.objects.get(id=1)),
                'view_user': view_user
            }
            return render(request, 'users/profile.html', context)
        else:
            return render(request, 'users/no-profile.html', {'exists': True})
    else:
        return render(request, 'users/no-profile.html', {'exists': False})


# class pfpChangeView(UpdateView, SuccessMessageMixin):
#     model=CustomUser
#     fields=['profile_pic']
#     template_name='users/pfp-change.html'
#     slug_field='kerberos'
#     success_url=f'/'
#     success_message='Your profile picture has been updated!'

class pfpChangeForm(forms.ModelForm):
    profile_pic = forms.ImageField()

    class Meta:
        model = CustomUser
        fields = ('profile_pic',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

@login_required(login_url='login')
def pfpChange(request):
    if request.method == 'POST':
        form = pfpChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile picture has been updated!')
            return redirect('dashboard')
    else:
        form = pfpChangeForm()
    return render(request, 'users/pfp-change.html', {'form': form})
    

# def handle_uploaded_file(u,f):
#     new_path=os.path.join('users/profile-pics', u.kerberos+'.'+f.name.split('.')[-1])
#     full_path=os.path.join(settings.MEDIA_ROOT,new_path)
#     if os.path.exists(full_path):
#         os.remove(full_path)
#     with open(full_path, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)



@login_required(login_url='login')
def pwdChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your password has been updated! Log in to continue')
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/pwd-change.html', {'form': form})


# @login_required(login_url='login')
# def profileEdit(request, k):
#     if request.user.kerberos==k:
#         if request.method == 'POST':
#             form = UserChangeForm(request.POST)
#             if form.is_valid():
#                 # r = Role.objects.get(id=3)
#                 form.save()
#                 # kerberos=form.cleaned_data.get('kerberos')
#                 # user=CustomUser.objects.get(kerberos=kerberos)
#                 # user.role.add(r)
#                 # user.save()
#                 messages.success(request, 'Your profile has been updated!')
#                 redirect(f'user/{k}')
#         else:
#             form = UserChangeForm()
#         return render(request, 'users/profile-edit.html', {'form': form})
#     redirect(f'user/{k}')
#     return HttpResponse('')