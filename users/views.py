from django.shortcuts import render,redirect

from .admin import UserCreationForm
from .models import Role, CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.urls import reverse


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
            return redirect(reverse('profile', args=[request.user.kerberos]))
    else:
        form = pfpChangeForm(instance=request.user)
    return render(request, 'users/pfp-change.html', {'form': form})
    

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
