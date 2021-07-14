from django.shortcuts import render
from django.shortcuts import render, redirect  	
from django.contrib.auth import authenticate, login, logout		
from django.contrib import messages		
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import NewComplaint

# Create your views here.

def loginStudent(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:	
            login(request, user)	

            if request.user:
                return redirect('student:studentDashboard')
        else:
            messages.info(request, 'ID OR Password is incorrect')		

    context = {}

    return render(request, 'student/login_student.html', context)
    

    
@login_required(login_url='/loginStudent')
def studentDashboard(request):
    # queryset = NewComplaint.objects.all().filter(complaint_status='PENDING')

    # context ={

    #     'pending_complaints': queryset
        
    # }
    
    return render(request, 'student/student_dashboard.html')

@login_required(login_url='/loginStudent')
def studentSubmitComplaint(request):
    if request.method == 'POST':
        first_name = request.user.first_name
        last_name = request.user.last_name
        full_name = first_name + " " + last_name
        print(request.POST)
        if request.POST.get('student_room_number') and request.POST.get('complaint_type') and request.POST.get('complaint_description') and request.POST.get('mobile_number'):
            complaint = NewComplaint()
            complaint.student_index_number = request.user.username
            complaint.student_full_name = full_name
            complaint.student_room_number = request.POST.get('student_room_number')
            complaint.complaint_type = request.POST.get('complaint_type')
            complaint.complaint_description = request.POST.get('complaint_description')
            complaint.mobile_number = request.POST.get('mobile_number')

            complaint.save()

            messages.success(request, "Thank you.")

            return redirect("student:studentViewAllComplaints")
        else:
            return render(request, "student/student_submit_complaint.html")    
    else:
        return render(request, "student/student_submit_complaint.html")


@login_required(login_url='/loginStudent')
def studentViewAllComplaints(request):
    return render(request, 'student/student_view_all_complaints.html')


@login_required(login_url='/loginStudent')
def studentViewAnnouncements(request):
    return render(request, 'student/student_view_announcements.html')