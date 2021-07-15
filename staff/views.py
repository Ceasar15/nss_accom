from django.shortcuts import render, redirect  	
from django.contrib.auth import authenticate, login, logout		
from django.contrib import messages		
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import PostAnnouncement
from .forms import PostAnnoumcementForm

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

def staffDashboard(request):
    return render(request, 'staff/staff_dashboard.html')

def staff_addNewStudent(request):
    return render(request, 'staff/add_new_student.html')

def staff_addNewVisitor(request):
    return render(request, 'staff/add_new_visitor.html')

def staff_postAnnouncement(request):

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