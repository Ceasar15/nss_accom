from django.http import request
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.db.models import Q

from .forms import SearchForm, RentalHouseForm, HouseHasForm, AmenitiesForm, RulesForm, PreferredTenantForm, HouseImagesForm, HouseImagesEditForm
from .models import NewRentalHouse, HouseHas, Amenities, PreferredTenant, Rules, HouseImages, SearchFilter
from users.models import Typed
from users.forms import UserTypeForm
from student.forms import StudentRegisterForm, UserContactFrom

import requests, pgeocode, pandas, json
from datetime import datetime


def check_user(user):
    if user.is_authenticated:
        typed = Typed.objects.filter(user_id=user).first()
        if typed.user_group == 'landlord':
            return user.first_name
    else:
        requesst = request
        return render(requesst, 'renting/login_NSS.html')

# def home_page(request):
#     # User logged in or not
#     if request.user.is_authenticated:
#         logged = True

#         #Getting the logged on user type 
#         try:
#             ut = request.user.ut.user_type	
#         except:
#             ut = None	

#     form = SearchForm()
#     log = 'false'
#     return render(request, 'renting/home.html', locals())


# def user_signin_status(request):
#     if request.user.is_authenticated:
#         return JsonResponse({'user':'logged_in'})

#     elif request.user.is_anonymous:
#         return JsonResponse({'user':'not_logged_in'})


def search_list(request):
    f = SearchFilter(request.GET, queryset=NewRentalHouse.objects.all())
    return render(request, 'renting/renting_house_results.html', {'filter': f})


def renting_house_results(request):
    house_list = NewRentalHouse.objects.all()
    city_query = request.GET.get('q')
    if city_query:
        print(city_query)
        house_list = house_list.filter(
            Q(city__icontains = city_query)).distinct()
        
        context = {
            'house_list': house_list,
        }
        return render(request,'renting/renting_house_results.html', context)
    else:
        return render(request, 'renting/renting_house_results.html')



# Make it as only post
# @login_required
def post_rent_ad(request):

    form = RentalHouseForm(initial={'country':'Ghana'}, data=request.POST or None)
    img_form = HouseImagesForm(files=request.FILES)
    PUB_KEY = settings.MAPBOX_PUBLIC_KEY
    if request.method == 'POST' and request.user.is_authenticated:
        if form.is_valid():
            rh_obj = form.save(commit=False)
            rh_obj.user = request.user
            rh_obj.save()
            if img_form.is_valid():
                for img_file in request.FILES.getlist('images'):
                    HouseImages.objects.create(images=img_file, nrh=rh_obj)
            else:
                print(img_form.errors)

            data = {'url':reverse_lazy('renting:house_amenities'),
                'id': rh_obj.id}

            return JsonResponse(data)

        else:
            form_errors = form.errors.items()
            print(form_errors)
            data = dict()
            if form_errors:
                for field,value in form_errors:
                    # print(field)
                    if field == 'house_no':
                        data.update({field:value[0]})
                    else:
                        data.update({field:value[0]})
            return JsonResponse(data, status=409)

    # GET Request
    elif request.user.is_anonymous:
        modl = 'true'
        return render(request, 'renting/rental_post.html', locals())

    # GET Request
    elif request.user.is_authenticated:
        # Saving the User_type
        try:
            ut = Typed.objects.get(user=request.user)
            ut_form = UserTypeForm(data={'user_type':'owner'},instance=ut)
        except:
            ut = None

        if ut:
            if ut_form.is_valid():
                ut_form.save()
        else:
            ut_form = UserTypeForm(data={'user_type':'owner'})
            if ut_form.is_valid():
                ut_obj = ut_form.save(commit=False)
                ut_obj.user = request.user
                ut_obj.save()

        return render(request, 'renting/rental_post.html', locals())



# @login_required
def update_rent_ad(request, id):
    if request.user.is_authenticated:
        try:
            print(request.POST)
            rh_obj = NewRentalHouse.objects.get(pk=id)
            form = RentalHouseForm(data=request.POST or None, instance=rh_obj)
            img_form = HouseImagesEditForm(files=request.FILES)
            print(form, img_form)
        except:
            rh_obj = None

        if request.method == 'POST' and rh_obj:
            if form.is_valid():
                nrh_obj = form.save()
                print(nrh_obj, img_form)
                if img_form.is_valid():
                    print(img_form)
                    for img_file in request.FILES.getlist('images'):
                        HouseImages.objects.create(images=img_file, nrh=nrh_obj)
                else:
                    print(img_form.errors)

            else:
                print(form.errors)
                # print('what else', form)
                data = {
                 'error':'check djangoconsole'
                }
                return JsonResponse(data, status=404)

            data = {'url':reverse_lazy('renting:house_amenities'),
                'id': nrh_obj.id}

            return JsonResponse(data)
        else:
            print(rh_obj)

    elif request.user.is_anonymous:
        modl='true'
        return HttpResponseRedirect(reverse('renting:edit_whole', args=(id,)))



# To get the HTML code of the House and Amenities
def get_ha_code(request):
    hform = HouseHasForm()
    aform = AmenitiesForm()
    return render(request, 'renting/house_has_and_amenities.html', locals())


def get_rp_code(request):
    rform = RulesForm()
    ptform = PreferredTenantForm()

    return render(request, 'renting/rules_and_preferred_tenant.html', locals())


def save_house_has(request, id):
    
    # print(id)
    try:
        nrh_obj = NewRentalHouse.objects.get(pk=id)
        hh_ex_obj = HouseHas.objects.filter(nrh=nrh_obj)
        if hh_ex_obj:
            hh_ex_form = HouseHasForm(data=request.POST or None, instance=hh_ex_obj[0])
            hh_form = None
        else:
            hh_form = HouseHasForm(data=request.POST or None)
        # print(nrh_obj)
    except:
        nrh_obj = None

    if request.method == 'POST' and nrh_obj:
        if hh_form is not None and hh_form.is_valid():
            hh_mod_obj = hh_form.save(commit=False)
            hh_mod_obj.nrh = nrh_obj
            hh_mod_obj.save()

            data = {
                'url':reverse_lazy('renting:house_amenities'),
                'hh_url':reverse_lazy('renting:house_has',args=(nrh_obj.id,))
            }
            # print(data['url'])
            return JsonResponse(data)

        elif hh_ex_form and hh_ex_form.is_valid():
            hh_ex_form.save()

            data = {
                'url':reverse_lazy('renting:house_amenities')
            }
            # print(data['url'])
            return JsonResponse(data)

        else:
            data = {
                'error':hh_form.errors.as_json()
            }
    # 		print(form.errors)
            return JsonResponse(data, status=400)

    else:
        return JsonResponse({
                'error':'Object not found'
            }, status=404)


def save_amenities(request, id):
    try:
        nrh_obj = NewRentalHouse.objects.get(pk=id)
        am_ex_obj = Amenities.objects.filter(nrh=nrh_obj)
        if am_ex_obj:
            a_ex_form = AmenitiesForm(data=request.POST or None, instance=am_ex_obj[0])
            a_form = None
        else:
            a_form = AmenitiesForm(data=request.POST or None)
    except:
        nrh_obj = None

    if request.method == 'POST' and nrh_obj:
        if a_form is not None and a_form.is_valid():
            a_mod_obj = a_form.save(commit=False)
            a_mod_obj.nrh = nrh_obj
            a_mod_obj.save()

            data = {
                'url':reverse_lazy('renting:rules_tenant'),
                'a_url':reverse_lazy('renting:save_amenities',args=(nrh_obj.id,))
            }
            # print(data['url'])
            return JsonResponse(data)

        elif a_ex_form and a_ex_form.is_valid():
            a_ex_form.save() 
            data = {
                'success':'posted'
            }

            return JsonResponse(data)
####### Handle the Json Error message in Jquery, Ajax + django
        else:
            print(a_form.errors)

def save_rules(request, id):
    try:
        nrh_obj = NewRentalHouse.objects.get(pk=id)
        rl_ex_obj = Rules.objects.filter(nrh=nrh_obj)
        if rl_ex_obj:
            r_ex_form = RulesForm(data=request.POST or None, instance=rl_ex_obj[0])
            r_form = None
        else:
            r_form = RulesForm(data=request.POST or None)
    except:
        nrh_obj = None

    if request.method == 'POST' and nrh_obj:
        if r_form is not None and r_form.is_valid():
            r_mod_obj = r_form.save(commit=False)
            r_mod_obj.nrh = nrh_obj
            r_mod_obj.save()

            data = {
                'url':reverse_lazy('renting:rules_tenant'),
                'r_url':reverse_lazy('renting:save_rules',args=(nrh_obj.id,))
            }
            # print(data['url'])
            return JsonResponse(data)
        elif r_ex_form and r_ex_form.is_valid():
            r_ex_form.save()
            data = {
                'success':'posted'
            }

            return JsonResponse(data)
        else:
            print(r_form.errors)



def save_pt(request, id):
    
    try:
        nrh_obj = NewRentalHouse.objects.get(pk=id)
        pt_ex_obj = PreferredTenant.objects.filter(nrh=nrh_obj)
        if pt_ex_obj:
            pt_ex_form = PreferredTenantForm(data=request.POST or None, instance=pt_ex_obj[0])
            pt_form = None
        else:
            pt_form = PreferredTenantForm(data=request.POST or None)
    except:
        nrh_obj = None

    if request.method == 'POST' and nrh_obj:
        if pt_form is not None and pt_form.is_valid():
            pt_mod_obj = pt_form.save(commit=False)
            pt_mod_obj.nrh = nrh_obj
            pt_mod_obj.save()

            data = {
                'url':reverse_lazy('renting:rules_tenant'),
                'e_url':reverse_lazy('renting:edit_whole',args=(nrh_obj.id,)),
                'd_url':reverse_lazy('renting:del_whole',args=(nrh_obj.id,)),
                'h_url':reverse_lazy('renting:house_details',args=(nrh_obj.id,)),
                'pt_url':reverse_lazy('renting:save_pt',args=(nrh_obj.id,))
            }
            return JsonResponse(data)

        elif pt_ex_form and pt_ex_form.is_valid():
            pt_ex_form.save()

            data = {
                'success':'posted'
            }

            return JsonResponse(data)

        else:
            print(pt_form.errors)	

# @login_required
def edit_whole(request, id):
    PUB_KEY = settings.MAPBOX_PUBLIC_KEY
    if request.user.is_authenticated:
        try:
            nrh_obj = NewRentalHouse.objects.get(pk=id)
            hh_fobj = HouseHas.objects.filter(nrh=nrh_obj)
            a_fobj = Amenities.objects.filter(nrh=nrh_obj)
            r_fobj = Rules.objects.filter(nrh=nrh_obj)
            pt_fobj = PreferredTenant.objects.filter(nrh=nrh_obj)
            img_qset = HouseImages.objects.filter(nrh=nrh_obj)

        except:
            nrh_obj = None
            # print(nrh_obj)
        
        if nrh_obj:
            images_list = []
            form = RentalHouseForm(instance=nrh_obj)
            img_form = HouseImagesEditForm()

            if img_qset:
                for img_obj in img_qset:
                    images_list.append(img_obj)
            if hh_fobj:
                hh_obj = hh_fobj[0]
                hform = HouseHasForm(instance=hh_obj)
            else:
                hform = HouseHasForm()
            if a_fobj:
                a_obj = a_fobj[0]
                aform = AmenitiesForm(instance=a_obj)
            else:
                aform = AmenitiesForm()
            if r_fobj:
                r_obj = r_fobj[0]
                rform = RulesForm(instance=r_obj)
            else:
                rform = RulesForm()
            if pt_fobj:
                pt_obj = pt_fobj[0]
                ptform = PreferredTenantForm(instance=pt_obj)
            else:
                ptform = PreferredTenantForm()

        return render(request, 'renting/rental_post_edit.html', locals())

    elif request.user.is_anonymous:
        modl = 'true'
        return render(request, 'renting/rental_post_edit.html', locals())

# @login_required
def delete_whole(request, id):
    if request.user.is_authenticated:
        try:
            nrh_obj = NewRentalHouse.objects.get(pk=id)
        except:
            nrh_obj = None

        if nrh_obj:
            nrh_obj.delete()
            return HttpResponseRedirect(reverse('renting:rent_ad_list'))

        # Need to handle the error for exception - object doesn't exists


    elif request.user.is_anonymous:
        modl='true'
        return HttpResponseRedirect(reverse('renting:edit_whole', args=(id,)))



def zipcode_validate(request):
    pl_zip = pgeocode.Nominatim('pl')

    try:
        zip_obj = pl_zip.query_postal_code(request.GET['zipcode'])
        # print(zip_obj, request.GET['zipcode'])
        cond = pandas.isna(zip_obj.community_name)
        # print(zip_obj)
    except:
        zip_obj = None

    if not cond:
        data = {
        'city' : zip_obj.community_name
        }
        # print(zip_obj.community_name)
        return JsonResponse(data)

    else:
        error = {
         'zipcode':'Enter a valid ZipCode'
        }
        # print(type(error))
        return JsonResponse(error, status=404)



def house_details(request, id):
    if request.user.is_authenticated:
        try:
            nrh_obj = NewRentalHouse.objects.get(pk=id)
            r_hh = HouseHas.objects.get(nrh=nrh_obj)
            am = Amenities.objects.get(nrh=nrh_obj)
            pt = PreferredTenant.objects.get(nrh=nrh_obj)
            rl = Rules.objects.get(nrh=nrh_obj)
            imgs = HouseImages.objects.filter(nrh=nrh_obj)
        except:
            nrh_obj = None

        if nrh_obj:
            return render(request, 'renting/house_detail.html', locals())

        ######### Handle the error for house object which doesn't exists

    elif request.user.is_anonymous:
        modl='true'
        return render(request, 'renting/house_detail.html', locals())

def rent_ads(request):
    if request.user.is_authenticated:
        house_list = NewRentalHouse.objects.filter(user=request.user)
        houses_list = []
        edit_list = []
        for hous_obj in house_list:
            try:
                rl = Rules.objects.get(nrh=hous_obj)
                pt = PreferredTenant.objects.get(nrh=hous_obj)
                am = Amenities.objects.get(nrh=hous_obj)
                hh = HouseHas.objects.get(nrh=hous_obj)
                proceed = True
            except:
                proceed = False

            if proceed:
                houses_list.append(hous_obj)
            else:
                edit_list.append(hous_obj)


        return render(request, 'renting/ads_list.html', locals())

    elif request.user.is_anonymous:
        modl='true'
        return render(request, 'renting/house_detail.html', locals())


def del_house_image(request,id):
    if request.user.is_authenticated:
        if request.method == 'DELETE':
            try:
                img_obj = HouseImages.objects.get(pk=id)
            except:
                img_obj = None

            if img_obj:
                img_obj.delete()

                return JsonResponse({'object':'deleted'})

            else:
                return JsonResponse({'object':'not_found'},status=404)



# the view for the first page of the nss accomodation.
def nssAccomFirstPage(request):
    return render(request, 'renting/index_NSS.html')



# the page for the landlord to register.
def registerAccount(request):
    form = StudentRegisterForm()
    user_contact_form =  UserContactFrom()
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        user_contact_form = UserContactFrom(request.POST)
        print(form)
        print(user_contact_form)
        if all((form.is_valid(), user_contact_form.is_valid() )):

            tt = form.save()
            print(tt.id)
            obs = user_contact_form.save(commit=False)
            obs.user_id_id = tt.id
            obs.save()

            return redirect('renting:signInLandlord')

    context = {
        'form': StudentRegisterForm(),
        'user_contact_form': UserContactFrom()
        }
    return render (request, 'renting/register.html', context)



# the sign in page for the landlord.
def signInLandlord(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:

            typed = Typed.objects.filter(user_id=user).first();
            if typed.user_group == 'landlord':
                login(request, user)	
                if request.user:
                    return redirect('renting:postRentAdds')
        else:
            messages.info(request, 'ID OR Password is incorrect')		

    context = {}

    return render(request, 'renting/login_NSS.html', context)


# the page where a landlord can view his rent adds.
@user_passes_test(check_user, login_url='/signInLandlord')
def viewRentAdds(request):
    house_list = NewRentalHouse.objects.all()
    city_query = request.GET.get('q')
    if city_query:
        print(city_query)
        house_list = house_list.filter(
            Q(city__icontains = city_query)).distinct()
        
        context = {
            'house_list': house_list,
        }
        return render(request,'renting/view_rent_adds.html', context)
    else:
        return render(request, 'renting/view_rent_adds.html')


# the page where a landlord can post his rent adds.
@user_passes_test(check_user, login_url='/signInLandlord')
def postRentAdds(request):
    form = RentalHouseForm(initial={'country':'Ghana'}, data=request.POST or None)
    img_form = HouseImagesForm(request.POST, files=request.FILES)
    house_has_form = HouseHasForm(request.POST)
    amenities_form = AmenitiesForm(request.POST)
    rules_form = RulesForm(request.POST)
    preferred_tenant_form = PreferredTenantForm(request.POST)

    if request.method == 'POST' and request.user.is_authenticated:
        if all((form.is_valid(), house_has_form.is_valid(), amenities_form.is_valid(), rules_form.is_valid(), preferred_tenant_form.is_valid())):
            rh_obj = form.save(commit=False)
            rh_obj.user = request.user
            rh_obj.save()
            nrh_obj = NewRentalHouse.objects.get(pk=rh_obj.id)
            if img_form.is_valid():
                for img_file in request.FILES.getlist('images'):
                    HouseImages.objects.create(images=img_file, nrh=nrh_obj)
                im = img_form.save(commit=False)
                im.nrh = nrh_obj
                im.save()
                hs = house_has_form.save(commit=False)
                hs.nrh = nrh_obj
                hs.save()
                amf = amenities_form.save(commit=False)
                amf.nrh = nrh_obj
                amf.save()
                rf = rules_form.save(commit=False)
                rf.nrh = nrh_obj
                rf.save()
                pf = preferred_tenant_form.save(commit=False)
                pf.nrh = nrh_obj
                pf.save()
            else:
                print(img_form.errors)
            
            return redirect('renting:landlordViewRentAds')


    # GET Request
    elif request.user.is_anonymous:
        modl = 'true'
        return render(request, 'renting/rental_post.html', locals())

    return render(request, 'renting/post_rent_adds.html', locals())



# check if student is authenticated
def check_student_user(user):
    if user.is_authenticated:
        typed = Typed.objects.filter(user_id=user).first()
        if typed.user_group == 'student':
            return user.first_name
    else:
        requesst = request
        return render(requesst,'student/login_student.html')


# the page where a student can view all rent ads.
@user_passes_test(check_student_user, login_url='/loginStudent')
def studentViewRentAds(request):
    f = SearchFilter(request.GET, queryset=NewRentalHouse.objects.all())
    return render(request, 'renting/student_view_rent_ads.html', {'filter': f})


# the page where a staff can view all rent ads.
def staffViewRentAds(request):
    return render(request, 'renting/staff_view_rent_ads.html')




# the page where a landlord can view all of their posted ads.
@user_passes_test(check_user, login_url='/signInLandlord')
def landlordViewRentAds(request):
    house_list = NewRentalHouse.objects.filter(user=request.user)
    houses_list = []
    edit_list = []
    for hous_obj in house_list:
        nrh_obj = NewRentalHouse.objects.filter(pk=hous_obj.id)
        try:
            rl = Rules.objects.get(nrh=hous_obj)
            pt = PreferredTenant.objects.get(nrh=hous_obj)
            am = Amenities.objects.get(nrh=hous_obj)
            hhh = HouseHas.objects.get(nrh=hous_obj)
            imgs = HouseImages.objects.filter(nrh=nrh_obj)
            proceed = True
        except:
            proceed = False

        if proceed:
            houses_list.append(hous_obj)
        else:
            edit_list.append(hous_obj)

    hh = HouseHas.objects.filter(nrh=nrh_obj)
    return render(request, 'renting/landlord_view_rent_ads.html', locals())



# the page where the landlord can see his own house details.
def landlordViewHouseDetails(request):
    return render(request, 'renting/landlord_view_own_ads_details.html')



# the page where the student can view the details of the ad.
def studentViewHouseDetails(request):
    return render(request, 'renting/student_view_ad_details.html')


