from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse

# Create your views here.
from django.urls import reverse
from threatify.models import *


def checkSession(request):
    if request.session.has_key('UserID'):
        return True
    return False


def signin(request):
    if checkSession(request):
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        context = {"Response": "", "Type": "text-danger"}
        if request.method == 'POST':
            form = request.POST
            Email = form.get('Email')
            Password = form.get('Password')
            Result = User.objects.filter(Email=Email, Password=Password)
            print(Result)
            if Result:
                request.session['UserID'] = Result[0].UserID
                # return HttpResponse('<h1>Show Dashboard</h1>')
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                context = {'Response': 'Invalid Email or Password...', "Type": "text-danger"}
        return render(request, 'threatify/SignIn.html', context)


def signup(request):
    # del request.session['UserID']
    if checkSession(request):
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        context = {"Response": "", "Type": "text-success"}
        if request.method == 'POST':
            print("REQUEST IS POST?")
            form = request.POST
            Name = form.get('Name')
            Email = form.get('Email')
            Password = form.get('Password')
            Object = User(Name=Name, Email=Email, Password=Password)
            Object.save()
            context = {"Response": "Registration Successful. Go to Sign In Page...", "Type": "text-success"}
            return render(request, 'threatify/SignUp.html', context)
        return render(request, 'threatify/SignUp.html')


def inverse(request, inverseForm):
    if inverseForm == "signin":
        return HttpResponseRedirect(reverse('signup'))
    elif inverseForm == "signup":
        return HttpResponseRedirect(reverse('signin'))


def logout(request):
    if checkSession(request):
        del request.session['UserID']
    return HttpResponseRedirect(reverse('signin'))


def dashboard(request):
    if checkSession(request):
        return render(request, 'threatify/Dashboard.html')
    return HttpResponseRedirect(reverse('signin'))


def camera(request):
    if checkSession(request):
        UserID = request.session['UserID']
        feedObjects = Feed.objects.filter(UserID=UserID)
        feedsUrl = []
        feedsId = []
        types = []
        for feed in feedObjects:
            feedsUrl.append(feed.Url)
            feedsId.append(feed.UserID)
            if 'youtube' in feed.Url:
                types.append('Youtube')
            else:
                types.append('CCTV')
        print(feedsId)
        print(feedsUrl)
        context = {
            "Feeds": zip(feedsId, feedsUrl,types)
        }
        return render(request, 'threatify/Camera.html', context)
    return HttpResponseRedirect(reverse('signin'))


def threatLog(request):
    if checkSession(request):
        return render(request, 'threatify/ThreatLog.html')
    return HttpResponseRedirect(reverse('signin'))


def settings(request):
    return HttpResponse('<h1>Show settings</h1>')
