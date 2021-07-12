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


def studentSignUp(request):
    return render(request, 'tracking/student_signup.html')


def studentDashboard(request):
    return render(request, 'tracking/student_dashboard.html')


def studentSubmitComplaint(request):
    return render(request, 'tracking/student_submit_complaint.html')


def studentViewAllComplaints(request):
    return render(request, 'tracking/student_view_all_complaints.html')


def studentViewAnnouncements(request):
    return render(request, 'tracking/student_view_announcements.html')

