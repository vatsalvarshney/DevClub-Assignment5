from django.shortcuts import render,redirect

from .admin import UserCreationForm
from .models import Role, CustomUser
from django.contrib import messages



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
            redirect('login')
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
            messages.success(request, f'Account Created For {kerberos}!')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

