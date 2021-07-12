from django.shortcuts import render, redirect  	
from django.contrib.auth import authenticate, login, logout		
from django.contrib import messages		
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import NewComplaint

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

@login_required(login_url='/usr/login')
def studentDashboard(request):
    return render(request, 'tracking/student_dashboard.html')

@login_required(login_url='/usr/login')
def studentSubmitComplaint(request):
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('fullname') and request.POST.get('email') and request.POST.get('phone') and request.POST.get('subject'):
            complaint = NewComplaint()
            complaint. = request.POST.get('fullname')
            complaint.fullname = request.POST.get('fullname')
            complaint.email = request.POST.get('email')
            complaint.phone = request.POST.get('phone')
            complaint.subject = request.POST.get('subject')
            complaint.save()

            messages.success(request, "Thank you.")

            return render(request, "tracking:studentViewAllComplaints")
            
    else:
        return render(request, "tracking/student_submit.html")

@login_required(login_url='/usr/login')
def studentViewAllComplaints(request):
    return render(request, 'tracking/student_view_all_complaints.html')

@login_required(login_url='/usr/login')
def studentViewAnnouncements(request):
    return render(request, 'tracking/student_view_announcements.html')

