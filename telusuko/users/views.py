from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth


# Create your views here.

def register(request):
    if request.method =='POST':
        firstname=request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        if User.objects.filter(username=username).exists():
            messages.info(request,'UserName already Taken')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email already Taken')

        elif pass1!=pass2:
            messages.info(request, 'confirm password is mismatched')

        else:
            user=User.objects.create_user(username=username,password=pass1,email=email,first_name=firstname,last_name=lastname)
            user.save()
            return redirect('login')
    return render(request,"register.html")

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        pass1 = request.POST['password']
        user = auth.authenticate(username=username,password=pass1)
        if user:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')