import tracking
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'tracking/indexxxx.html')


def loginStudent(request):
    return render(request, 'tracking/login.html')


def loginStaff(request):
    return render(request, 'tracking/login_staff.html')


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


def staffDashboard(request):
    return render(request, 'tracking/staff_dashboard.html')


def addNewStudent(request):
    return render(request, 'tracking/add_new_student.html')


def addNewVisitor(request):
    return render(request, 'tracking/add_new_visitor.html')


def postAnnouncement(request):
    return render(request, 'tracking/post_announcement.html')


