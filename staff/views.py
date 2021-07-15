from django.shortcuts import render, redirect  	
from django.contrib.auth import authenticate, login, logout		
from django.contrib import messages		
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def loginStaff(request):
    
    if request.method == 'POST':

        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:	
            login(request, user)	

            if request.user:
                return redirect('staff:staffDashboard')

        else:
            messages.info(request, 'ID OR Password is incorrect')		

    context = {}

    return render(request, 'staff/login_staff.html', context)

<<<<<<< HEAD
@login_required(login_url='/loginStaff')
||||||| ed5ec9d
=======

>>>>>>> 267ab626ae90cefc7d1800b7691d4e1fd8114605
def staffDashboard(request):
    return render(request, 'staff/staff_dashboard.html')

<<<<<<< HEAD

@login_required(login_url='/loginStaff')
||||||| ed5ec9d
=======

>>>>>>> 267ab626ae90cefc7d1800b7691d4e1fd8114605
def staff_addNewStudent(request):
    return render(request, 'staff/add_new_student.html')

<<<<<<< HEAD

@login_required(login_url='/loginStaff')
||||||| ed5ec9d
=======

>>>>>>> 267ab626ae90cefc7d1800b7691d4e1fd8114605
def staff_addNewVisitor(request):
    return render(request, 'staff/add_new_visitor.html')

<<<<<<< HEAD

@login_required(login_url='/loginStaff')
||||||| ed5ec9d
=======

>>>>>>> 267ab626ae90cefc7d1800b7691d4e1fd8114605
def staff_postAnnouncement(request):
    return render(request, 'staff/post_announcement.html')
