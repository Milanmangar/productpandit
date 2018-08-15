from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from products.models import Product
from django.contrib import messages


def signup(request):
    if request.method=='POST':
        if request.POST['password1']==request.POST['password2']:
            #checking if username is already present in database,below code
            #will return username if there is one
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request,'accounts/signup.html',{'error':'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request,'accounts/signup.html',{'error':'Password didnot match'})

    else:

        return render(request,'accounts/signup.html')

def login(request):
    if request.method=='POST':
        #below is checking the authentication returns none if user and password doesnt match
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:

            messages.error(request,'username or password is incorrect')

            return redirect('home')

    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('home')
