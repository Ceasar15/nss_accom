import tracking
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'tracking/indexxxx.html')


def loginStudent(request):
    return render(request, 'tracking/login.html')


def loginStaff(request):
    return render(request, 'tracking/login_staff.html')


def studentSubmitComplaint(request):
    return render(request, 'tracking/student_submit.html')