from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from account.models import Profile

# Create your views here.
def signup(request):
    content = {}
    content['title'] = 'Signup'
    if request.method == 'POST':
        try:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
            user.save()
            last_user = User.objects.latest('id')
            profile = Profile()
            profile.mobile = request.POST['mobile']
            profile.user = User.objects.get(pk=int(last_user.id))
            profile.save()
            messages.success(request, "Signup successfully. You can login now.")
            return HttpResponseRedirect(reverse('login'))
        except IntegrityError:
            messages.error(request, "Username already exists. Please choose a different one.")
            return HttpResponseRedirect(reverse('signup'))
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return HttpResponseRedirect(reverse('signup'))
    return render(request, 'signup.html', content)

def login(request):
    content = {}
    content['title'] = 'Login'
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, "Invalid credentials.")
            return HttpResponseRedirect(reverse('login'))
    return render(request, 'login.html', content)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))