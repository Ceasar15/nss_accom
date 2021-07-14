from django.shortcuts import render, redirect  	
from django.contrib.auth import authenticate, login, logout		
from django.contrib import messages		
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



# Create your views here.

def index(request):
    return render(request, 'tracking/indexxxx.html')


def loginStudent(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:	
            login(request, user)	

            if request.user:
                return redirect('tracking:studentDashboard')
            else:
                return redirect('tracking:studentSubmitComplaint')

        else:
            messages.info(request, 'ID OR Password is incorrect')		

    context = {}

    return render(request, 'tracking/login.html', context)

def loginStaff(request):
    return render(request, 'tracking/login_staff.html')



