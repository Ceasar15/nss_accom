from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect	
from django.contrib.auth import authenticate, login, logout		
from django.contrib import messages		
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.urls.base import reverse

from .forms import NewStudentForm, PostAnnoumcementForm, NewVisitorForm, UpdateVisitorForm
from .models import NewStudent, NewVisitor, PostAnnouncement
from student.models import NewComplaint
from users.models import Typed


def check_user(user):
    if user.is_authenticated:
        typed = Typed.objects.filter(user_id=user).first()
        if typed.user_group == 'staff':
            return user.first_name
    else:
        requesst = request
        return render(requesst,'staff/login_staff.html')



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
    # total_student = NewStudent.objects.filter()
    total_student = NewStudent.objects.all().count()
    # total_student= NewStudent.objects.filter(student_hall=)
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
        #print(s_form.last_name)
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
        # print(request.first_name)
        #print(s_form)
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
def list_viewVisitor(request):
    dataset = NewVisitor.objects.all()
    context = {
        'dataset': dataset
    }
    return render(request, 'staff/list_visitor.html', context)



@user_passes_test(check_user, login_url='/loginStaff')
def detail_viewVisitor(request, vistor_id):

    data = NewVisitor.objects.all()
    print(data)
    
    context = {
        'data': data
    }

    return render(request, 'staff/detail_visitor.html', context)



@user_passes_test(check_user, login_url='/loginStaff')
def update_viewVisitor(request, vistoor_id):
    
    obj = get_object_or_404(NewVisitor, vistor_id=vistoor_id)

    form = NewVisitor(request.POST or None, instance= obj )

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/"+vistoor_id)

    context = {

        'form': form
   
    }
    return render(request, 'staff/update_visitor.html', context)



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


@user_passes_test(check_user, login_url='/loginStaff')
def updateVisitorStatus(request):
    # user = request.newvisitor
    form = UpdateVisitorForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            print("Update Fine")
            return redirect('staff:staffDashboard')
        else:
            print("error")
    else:
        print("GET profile.html")
    context = {

        "update_visitor" : form,
    }
    return render(request, 'staff/update_visitor.html', context)