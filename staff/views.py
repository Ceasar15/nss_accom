from django.shortcuts import render, redirect  	
from django.contrib.auth import authenticate, login, logout		
from django.contrib import messages		
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from .forms import NewStudentForm, PostAnnoumcementForm, NewVisitorForm
from .models import NewStudent, NewVisitor, PostAnnouncement
from student.models import NewComplaint
from users.models import Typed


def check_user(user):
    typed = Typed.objects.filter(user_id=user).first()
    if typed.user_group == 'staff':
        return user.first_name


def loginStaff(request):
    
    if request.method == 'POST':

        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            typed = Typed.objects.filter(user_id=user).first();
            if typed.user_group == 'staff':
                login(request, user)	
                if request.user:
                    return redirect('staff:staffDashboard')
        else:
            messages.info(request, 'ID OR Password is incorrect')		

    context = {}

    return render(request, 'staff/login_staff.html', context)


@user_passes_test(check_user, login_url='/loginStaff')
def staffDashboard(request):
    total_student = NewStudent.objects.all().count()
    total_visitors = NewVisitor.objects.all().count()
    total_complains = NewComplaint.objects.all().count()

    context = {
        
        'total_student' : total_student,
        'total_visitors': total_visitors,
        'total_complains': total_complains,

    }

    return render(request, 'staff/staff_dashboard.html', context)


@user_passes_test(check_user, login_url='/loginStaff')
def staff_addNewStudent(request):
    if request.method == 'POST':
        s_form = NewStudentForm(request.POST, files=request.FILES)
        if s_form.is_valid():
            
            sform = s_form.save(commit=False)
            sform.save()

            messages.success(request, f'New Student Added')

            return redirect('staff:staffDashboard')
        
    context = {
        's_form': NewStudentForm(),
    }

    return render(request, 'staff/add_new_student.html', context)


@user_passes_test(check_user, login_url='/loginStaff')
def staff_addNewVisitor(request):
    if request.method == 'POST':
        s_form = NewVisitorForm(request.POST)
        if s_form.is_valid():
        
            sform = s_form.save(commit=False)
            sform.save()

            messages.success(request, f'Visitor Recorded')

            return redirect('staff:staffDashboard')
        
    context = {
        's_form': NewVisitorForm(),
    }
    return render(request, 'staff/add_new_visitor.html', context)


@user_passes_test(check_user, login_url='/loginStaff')
def staffPostAnnouncement(request):
    if request.method == 'POST':
        p_form = PostAnnoumcementForm(request.POST)
        if p_form.is_valid():
            obj = p_form.save(commit=False)
            obj.annou_user = request.user
            obj.save()
            messages.success(request, f'Your Announcement has been Updated Successfully')
            
            return redirect('staff:staffDashboard')
    
    context={
    
            'p_form': PostAnnoumcementForm()
    
            }
        
    return render(request, 'staff/post_announcement.html', context)

