from django.contrib.auth.models import User
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect	
from django.contrib.auth import authenticate, login		
from django.contrib import messages		
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone

from notifications.signals import notify

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
    typed = Typed.objects.filter(user_id=request.user).first()
    total_student = NewStudent.objects.filter(hall=typed.student_hall).count()
    total_visitors = NewVisitor.objects.filter(hall=typed.student_hall).count()
    total_complains = NewComplaint.objects.filter(student_hall=typed.student_hall).count()

    context = {
        
        'total_student' : total_student,
        'total_visitors': total_visitors,
        'total_complains': total_complains,

    }

    return render(request, 'staff/staff_dashboard.html', context)


@user_passes_test(check_user, login_url='/loginStaff')
def staff_addNewStudent(request):
    if request.method == 'POST':
        typed = Typed.objects.filter(user_id=request.user).first()
        s_form = NewStudentForm(request.POST, files=request.FILES, initial={'hall': typed.student_hall})
        print(s_form)
        if s_form.is_valid():
            
            sform = s_form.save(commit=False)
            sform.hall = typed.student_hall
            sform.save()

            messages.success(request, f'New Student Added Successfully.')

            return redirect('staff:addNewStudent')
        
    context = {
        's_form': NewStudentForm(),
    }

    return render(request, 'staff/add_new_student.html', context)


@user_passes_test(check_user, login_url='/loginStaff')
def staff_addNewVisitor(request):
    if request.method == 'POST':
        typed = Typed.objects.filter(user_id=request.user).first()
        s_form = NewVisitorForm(request.POST, initial={'hall': typed.student_hall})
        if s_form.is_valid():
        
            sform = s_form.save(commit=False)
            sform.hall = typed.student_hall
            sform.save()

            messages.success(request, f'Visitor Recorded Successfully!')

            return redirect('staff:addNewVisitor')
        
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

    form = NewVisitor(request.POST or None, instance=obj )

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/"+vistoor_id)

    context = {

        'form': form
   
    }
    return render(request, 'staff/update_visitor.html', context)

# def my_handler(sender, instance, created, **kwargs):
#     print(sender)
#     typed = Typed.objects.filter(user_id=request.user).first()
#     user = User.objects.get(hall=typed.student_hall)
#     print(user)
#     notify.send(user, recipient=user, verb='new announcement posted')

# post_save.connect(my_handler, sender=PostAnnouncement)


@user_passes_test(check_user, login_url='/loginStaff')
def staffPostAnnouncement(request):
    if request.method == 'POST':
        p_form = PostAnnoumcementForm(request.POST)
        if p_form.is_valid():
            obj = p_form.save(commit=False)
            obj.annou_user = request.user
            obj.save()
            messages.success(request, f'Your Announcement has been Posted Successfully')
            typed = Typed.objects.filter(user_id=request.user).first()
            user_list = []
            user_list = PostAnnouncement.objects.filter(hall=typed.student_hall)
            print(user_list)
            notify.send(request.user, recipient=user_list, verb='new announcement posted')
            return redirect('staff:staffPostAnnouncement')
    context={
            'p_form': PostAnnoumcementForm()
            }
    return render(request, 'staff/post_announcement.html', context)


@user_passes_test(check_user, login_url='/loginStaff')
def updateVisitorStatus(request):
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


# staff view all students.
@user_passes_test(check_user, login_url='/loginStaff')
def staffViewAllStudents(request):
    typed = Typed.objects.filter(user_id=request.user).first()
    dataset = NewStudent.objects.filter(hall=typed.student_hall)
    context = {
        'dataset': dataset,
    }
    return render(request, 'staff/staff_view_all_students.html', context)


@user_passes_test(check_user, login_url='/loginStaff')
def check_in(request, id):
    student = get_object_or_404(NewStudent, id=id)
    student.check_in = True
    student.save()
    return redirect('staff:staffViewAllStudents')


# staff view all visitors.
@user_passes_test(check_user, login_url='/loginStaff')
def staffManageVisitors(request):
    typed = Typed.objects.filter(user_id=request.user).first()
    dataset = NewVisitor.objects.filter(hall=typed.student_hall)
    context = {
        'dataset': dataset,
    }
    return render(request, 'staff/staff_manage_visitors.html', context)


@user_passes_test(check_user, login_url='/loginStaff')
def leave(request, vistor_id):
    visitor = get_object_or_404(NewVisitor, vistor_id=vistor_id)
    visitor.departed_at = timezone.now()
    visitor.save()
    return redirect('staff:staffManageVisitors')



# staff view all complaints.
@user_passes_test(check_user, login_url='/loginStaff')
def staffViewAllComplaints(request):
    typed = Typed.objects.filter(user_id=request.user).first()
    dataset = NewComplaint.objects.filter(student_hall=typed.student_hall)
    context = {
        'dataset': dataset,
    }
    return render(request, 'staff/staff_view_all_complaints.html', context)
    


@user_passes_test(check_user, login_url='/loginStaff')
def solved(request, complaint_id):
    typed = Typed.objects.filter(user_id=request.user).first()
    complaint = get_object_or_404(NewComplaint, complaint_id=complaint_id, student_hall=typed.student_hall)
    complaint.complaint_status = 'RESOLVED'
    complaint.save()
    return redirect('staff:staffViewAllComplaints')