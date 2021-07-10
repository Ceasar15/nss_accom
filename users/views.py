from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

from users.forms import UserTypeForm, UserForm, UpdatePhoneNo
from users.models import UserType


from django.http import HttpResponse
from django.shortcuts import render, redirect
from users.forms import RegisterForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.




# Create your views here.


def welcome(request):
    return HttpResponse('Welcome page renders out')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracking:index')

    context = {'form': RegisterForm()}
    return render(request, 'tracking/register.html', context)


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
			ut = UserType.objects.get(user=request.user)
		except:
			ut = None

		if request.method == 'POST' and ut:
			utform = UserTypeForm(data=request.POST, instance=ut)
			if utform.is_valid():
				ut_obj = utform.save()
			else:
				print(ut_form.erros)

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