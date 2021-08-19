from staff.forms import StaffProfileForm
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

from users.forms import ContactForm, UserTypeForm, UserForm, UpdatePhoneNo,ProfileForm
from users.models import Profile, Typed


from django.http import HttpResponse
from django.shortcuts import render, redirect
from student.forms import StudentProfileForm, StudentRegisterForm, EditProfileForm, UserContactFrom
from users.forms import StaffRegisterForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def Studentregister(request):

    form = StudentRegisterForm()
    user_contact_form =  UserContactFrom()
    student_profile = StudentProfileForm()
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        user_contact_form = UserContactFrom(request.POST)
        student_profile = StudentProfileForm(request.POST, request.FILES)
        if all((form.is_valid(), user_contact_form.is_valid(), student_profile.is_valid() )):
            #save user
            user = form.save()
            # user.refresh_from_db()
            #student_profile
            spf = student_profile.save(commit=False)
            spf.user_id = user.id
            spf.save()
            # user.save()
            # user_contact_form
            obs = user_contact_form.save(commit=False)
            obs.user_id_id = user.id
            obs.user_group = 'student'
            username = user.first_name
            obs.save()
            
            #auto login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.info(request, f"You are now logged in as {username}")
            return redirect('student:studentDashboard')

        else:
            password1 = form.data['password1']
            password2 = form.data['password2']
            email = form.data['email']
            print(form.errors)
            for msg in form.errors.as_data():
                if msg == 'email':
                    messages.error(request, f"Your email: {email} is not valid")
                if msg == 'password2' and password1 == password2:
                    messages.error(request, f"The selected password is not strong enough. Mininum of 8 Characters")
                elif msg == 'password2' and password1 != password2:
                    messages.error(request, f"Password and Confirmation Password do not match")

    context = {
        'form': StudentRegisterForm(),
        'user_contact_form': UserContactFrom(),
        'student_profile' : StudentProfileForm()

        }

    return render(request, 'tracking/sign_up.html', context)


def StaffRegister(request):
    
    form = StudentRegisterForm()
    user_contact_form =  UserContactFrom()
    staff_profile = StaffProfileForm()

    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        user_contact_form = UserContactFrom(request.POST)
        staff_profile = StaffProfileForm(request.POST, request.FILES)
        if all((form.is_valid(), user_contact_form.is_valid(), staff_profile.is_valid() )):
            # save user
            user = form.save()
            # user.refresh_from_db()
            # staff profile
            stf = staff_profile.save(commit=False)
            stf.user_id = user.id
            stf.save()
            # user.save()
            # user contact form
            obs = user_contact_form.save(commit=False)
            obs.user_id_id = user.id
            obs.user_group = 'staff'
            username = user.first_name
            obs.save()

            # auto login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.info(request, f"You are now logged in as {username}")
            return redirect('staff:staffDashboard')

        else:
            password1 = form.data['password1']
            password2 = form.data['password2']
            email = form.data['email']
            print(form.error_messages)
            for msg in form.errors.as_data():
                if msg == 'email':
                    messages.error(request, f"Your email: {email} is not valid")
                if msg == 'password2':
                    messages.error(request, f"Your password can’t be too similar to your other personal information!")
                elif msg == 'password2' and password1 != password2:
                    messages.error(request, f"Password and Confirmation Password do not match")

    context = {
        'form': StudentRegisterForm(),
        'user_contact_form': UserContactFrom(),
        'staff_profile' : StaffProfileForm()

        }

    return render(request, 'tracking/sign_up_staff.html', context)


def LandlordRegister(request):
    
    form = StudentRegisterForm()
    user_contact_form =  UserContactFrom()
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        user_contact_form = UserContactFrom(request.POST)
        profile_form = Profile()
        if all((form.is_valid(), user_contact_form.is_valid() )):
            user = form.save()
            obs = user_contact_form.save(commit=False)
            obs.user_id_id = user.id
            obs.user_group = 'landlord'
            profile_form.user_id =  user.id
            profile_form.location = 'dummy location'
            profile_form.occupation = 'dummy_occupation'
            profile_form.save()
            obs.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('renting:landlordProfile',  id=user.id)

        else:
            password1 = form.data['password1']
            password2 = form.data['password2']
            email = form.data['email']
            for msg in form.errors.as_data():
                if msg == 'email':
                    messages.error(request, f"Your email: {email} is not valid")
                if msg == 'password2':
                    messages.error(request, f"Your password can’t be too similar to your other personal information!")
                elif msg == 'password2' and password1 != password2:
                    messages.error(request, f"Password and Confirmation Password do not match")
    
    context = {
        'form': StudentRegisterForm(),
        'user_contact_form': UserContactFrom()
        }

    return render(request, 'tracking/sign_up_landlord.html', context)


@login_required(login_url='/usr/login')
def profile(request):
    context = {'user': request.user}
    return render(request, 'users/settings.html', context)


@login_required(login_url='/usr/login')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('auth:welcome')

    context = {'form': EditProfileForm(instance=request.user)}
    return render(request, 'authapp/edit_profile.html', context)


@login_required(login_url='/usr/login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('tracking:index')

    context = {'form': PasswordChangeForm(user=request.user)}
    return render(request, 'tracking/password_change_form.html', context)


@login_required(login_url='/usr/login')
def logout_view(request):
    logout(request)
    return redirect('users:login')

def user_type(request):
    if request.user.is_authenticated:
        try:
            ut = Typed.objects.get(user=request.user)
        except:
            ut = None

        if request.method == 'POST' and ut:
            utform = UserTypeForm(data=request.POST, instance=ut)
            if utform.is_valid():
                ut_obj = utform.save()
            else:
                print(utform.erros)

            # Handle the form errors

            return JsonResponse({'user_type':ut_obj.user_type.capitalize()})

            
        elif request.method == 'POST':
            utform = UserTypeForm(data=request.POST)
            if utform.is_valid():
                ut_obj = utform.save(commit=False)
                ut_obj.user = request.user
                ut_obj.save()

            # Handle the form errors
            
            return JsonResponse({'user_type':ut_obj.user_type.capitalize()})
            
    else:
        return JsonResponse({'data':'error'},status=404)


def settings(request):
    usr = request.user
    form = UserForm(instance=usr)
    try:
        pno = usr.contactdetails
        # print(pno, usr.contactdetails)
        pform = UpdatePhoneNo(instance=pno)
    except:
        pno = None
        pform = UpdatePhoneNo()

    if request.method == 'POST':
        pform = UpdatePhoneNo(data=request.POST, instance=pno)
        form = UserForm(data=request.POST, instance=usr)
        if pform.is_valid():
            p_obj = pform.save(commit=False)
            p_obj.user = request.user
            p_obj.save()

        if form.is_valid():
            form.save()

        return render(request, 'users/settings.html', locals())
    
    else:
        return render(request, 'users/settings.html', locals())


def account_delete(request):
    usr_obj = User.objects.get(id=request.user.id)
    usr_obj.delete()

    return HttpResponseRedirect(reverse('renting:home'))


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Messages Sent!')
            return redirect('users:contact')

    context = {
        'form': ContactForm()
    }
    
    return render(request, 'users/contact.html', context)

from django.contrib.auth.password_validation import UserAttributeSimilarityValidator