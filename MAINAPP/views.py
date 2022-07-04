from ast import Global
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

global showsuccess
global processStatus
global connectionStatus
showsuccess=''
processStatus=''
connectionStatus=''

# Create your views here.
def home(request):
    global showsuccess
    global processStatus
    global connectionStatus
    showsuccess=''
    processStatus=''
    connectionStatus=''
    return render(request, "MAINAPP/home.html")

def terminal(request):
    global showsuccess
    global processStatus
    global connectionStatus
    return render(request, "MAINAPP/terminal.html", {'connectionStatus': connectionStatus,
                             'processStatus': processStatus})

def about(request):
    return render(request, "MAINAPP/about.html")

def about2(request):
    return render(request, "MAINAPP/about2.html")

def signup(request):
    global showsuccess

    if request.method == "POST":
        #username = request.POST.get('username')        #you can also get the variables using this method also...
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']
        agree = request.POST['agree']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        showsuccess = 'warning'
        messages.success(request, "Your account has been sucessfully created")

        return redirect('signin')


    return render(request, "MAINAPP/signup.html")

def signin(request):
    global showsuccess
    global username

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['password']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            global fname
            global lname
            global email
            fname = user.first_name
            lname = user.last_name
            email = user.email
            username = user.username
            return redirect('dashboard')

        else:
            showsuccess = 'warning'
            messages.error(request, "Invalid login credentials!")
            return redirect('signin')

    return render(request, "MAINAPP/signin.html")     

def signout(request):
    logout(request)
    global showsuccess
    showsuccess = 'sucess'
    messages.success(request, "Logged out sucessful")
    return redirect('Welcome Page')

def dashboard(request):
    global fname
    global lname
    global username
    global email
    return render(request, "MAINAPP/dashboard.html", {'fname': fname, 'lname': lname, 'username': username, 'email': email})

def connect(request):
    global showsuccess
    global connectionStatus
    if connectionStatus == 'Disconnected' or connectionStatus == '':
        connectionStatus='Connected'
        showsuccess = 'sucess'
        messages.success(request, "Connected Sucessfully")
        return redirect('terminal')
    elif connectionStatus == 'Connected':
        showsuccess = 'warning'
        messages.error(request, "Device is already connected!")
        return redirect('terminal')

def disconnect(request):
    global showsuccess
    global connectionStatus
    if processStatus == 'Started':
        showsuccess = 'warning'
        messages.error(request, "Operation in progress")
        return redirect('terminal')
    elif connectionStatus == '':
        showsuccess = 'warning'
        messages.error(request, "Device is not connected!")
        return redirect('terminal')
    elif connectionStatus == 'Disconnected':
        showsuccess = 'warning'
        messages.error(request, "Device already disconnected!")
        return redirect('terminal')
    else:
        connectionStatus='Disconnected'
        return redirect('terminal')

def enable(request):
    global showsucess
    if connectionStatus == 'Connected':
        global processStatus
        processStatus='Started'
        showsuccess = 'sucess'
        messages.success(request, "Process started")
        return redirect('terminal')
    else:
        showsuccess = 'warning'
        messages.error(request, "Device not connected")
        return redirect('terminal')

def disable(request):
    global showsuccess
    global processStatus
    if connectionStatus == 'Connected' and processStatus is not '':
        processStatus='Ended'
        showsuccess = 'sucess'
        messages.success(request, "Process ended")
        return redirect('terminal')
    else:
        showsuccess = 'warning'
        messages.error(request, "Process not started")
        return redirect('terminal')
    
