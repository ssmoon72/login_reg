from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'login/index.html')

def registration(request):
    validationCheck = User.usermanager.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm_password'])
    if 'theUser' in validationCheck:
        messages.success(request, 'Successfully registered,' + ' ' + request.POST['first_name'])
        return redirect('/success')
    elif 'errors' in validationCheck:
        for message in validationCheck['errors']:
            messages.error(request, message)
        return redirect('/')

def login(request):
    loginCheck = User.usermanager.login(request.POST['email'], request.POST['password'])
    if 'theUser' in loginCheck:
        messages.success(request, 'Successfully Logged In')
        return redirect ('/success')
    if 'errors' in loginCheck:
        for message in loginCheck['errors']:
            messages.error(request, message)
        return redirect('/')

def success(request):
    context ={
    'users': User.usermanager.all()
    }
    return render(request, 'login/success.html', context)
