from django.shortcuts import render, redirect  	
from django.contrib.auth import authenticate, login, logout		
from django.contrib import messages		

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

            if request.user.is_student:
                return redirect('tracking/student_submit.html')
            else:
                return redirect('tracking/student_submit.html')

        else:
            messages.info(request, 'ID OR Password is incorrect')		

    context = {}

    return render(request, 'tracking/login.html', context)


def loginStaff(request):
    return render(request, 'tracking/login_staff.html')


def studentSubmitComplaint(request):
    return render(request, 'tracking/student_submit.html')