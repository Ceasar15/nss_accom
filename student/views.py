from django.http import request
from users.models import Typed
from django.shortcuts import render
from django.shortcuts import render, redirect  	
from django.contrib.auth import authenticate, login, logout		
from django.contrib import messages		
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User



from .models import NewComplaint

# Create your views here.
def check_user(user):
    if user.is_authenticated:
        typed = Typed.objects.filter(user_id=user).first()
        if typed.user_group == 'student':
            return user.first_name
    else:
        requesst = request
        return render(requesst,'student/login_student.html')



def loginStudent(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            typed = Typed.objects.filter(user_id=user).first();
            if typed.user_group == 'student':
                login(request, user)	
                if request.user:
                    return redirect('student:studentDashboard')
        else:
            messages.info(request, 'ID OR Password is incorrect')		

    context = {}

    return render(request, 'student/login_student.html', context)
    


@user_passes_test(check_user, login_url='/loginStudent')
def studentDashboard(request):
    typed = Typed.objects.filter(user_id=request.user).first()
    total_complains = NewComplaint.objects.filter(student_hall=typed.student_hall).count()
    pending = NewComplaint.objects.filter(complaint_status='PENDING', student_hall=typed.student_hall).count()
    resolved = NewComplaint.objects.filter(complaint_status='RESOLVED', student_hall=typed.student_hall).count()

    context = {

        'total_complains': total_complains,
        'pending': pending,
        'resolved': resolved,

    }
    
    return render(request, 'student/student_dashboard.html', context)


@user_passes_test(check_user, login_url='/loginStudent')
def studentSubmitComplaint(request):
    if request.method == 'POST':
        first_name = request.user.first_name
        last_name = request.user.last_name
        full_name = first_name + " " + last_name
        typed = Typed.objects.filter(user_id=request.user).first()
        print(request.POST)
        if request.POST.get('student_room_number') and request.POST.get('complaint_type') and request.POST.get('complaint_description') and request.POST.get('mobile_number'):
            complaint = NewComplaint()
            complaint.student_index_number = request.user.username
            complaint.student_full_name = full_name
            complaint.student_room_number = request.POST.get('student_room_number')
            complaint.complaint_type = request.POST.get('complaint_type')
            complaint.complaint_description = request.POST.get('complaint_description')
            complaint.mobile_number = request.POST.get('mobile_number')
            complaint.student_hall = typed.student_hall

            complaint.save()

            messages.success(request, "Thank you.")

            return redirect("student:studentViewAllComplaints")
        else:
            return render(request, "student/student_submit_complaint.html")    
    else:
        context = {
            'neww' : NewComplaint()
        }
        return render(request, "student/student_submit_complaint.html", context)


@user_passes_test(check_user, login_url='/loginStudent')
def studentViewAllComplaints(request):
    typed = Typed.objects.filter(user_id=request.user).first()
    dataset = NewComplaint.objects.filter(student_hall=typed.student_hall)


    context = {
        'dataset': dataset,
    }

    return render(request, 'student/student_view_all_complaints.html', context)

@user_passes_test(check_user, login_url='/loginStudent')
def studentViewAnnouncements(request):
    return render(request, 'student/student_view_announcements.html')
