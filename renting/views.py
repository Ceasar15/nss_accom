from .forms import PaymentsForm
from users.forms import ProfileForm
from users.models import Typed, Profile
from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.urls.base import is_valid_path

from .forms import ContactLandlordForm, RentalHouseForm, HouseHasForm, AmenitiesForm, RulesForm, PreferredTenantForm, HouseImagesForm, HouseImagesEditForm, RatingForm
from .models import NewRentalHouse, HouseHas, Amenities, PreferredTenant, Rating, Rules, HouseImages, SearchFilter
from users.models import Profile, Typed
from student.forms import StudentRegisterForm, UserContactFrom


def check_user(user):
    if user.is_authenticated:
        typed = Typed.objects.filter(user_id=user).first()
        if typed.user_group == 'landlord':
            return user.first_name
    else:
        requesst = request
        return render(requesst, 'renting/login_NSS.html')


def search_list(request):
    f = SearchFilter(request.GET, queryset=NewRentalHouse.objects.all())
    return render(request, 'renting/renting_house_results.html', {'filter': f})


def renting_house_results(request):
    house_list = NewRentalHouse.objects.all()
    city_query = request.GET.get('q')
    if city_query:
        print(city_query)
        house_list = house_list.filter(
            Q(city__icontains=city_query)).distinct()

        context = {
            'house_list': house_list,
        }
        return render(request, 'renting/renting_house_results.html', context)
    else:
        return render(request, 'renting/renting_house_results.html')


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
                        HouseImages.objects.create(
                            images=img_file, nrh=nrh_obj)
                else:
                    print(img_form.errors)

            else:
                print(form.errors)
                # print('what else', form)
                data = {
                    'error': 'check djangoconsole'
                }
                return JsonResponse(data, status=404)

            data = {'url': reverse_lazy('renting:house_amenities'),
                    'id': nrh_obj.id}

            return JsonResponse(data)
        else:
            print(rh_obj)

    elif request.user.is_anonymous:
        modl = 'true'
        return HttpResponseRedirect(reverse('renting:edit_whole', args=(id,)))


@user_passes_test(check_user, login_url='/signInLandlord')
def edit_whole(request, id):
    nrh_obj = NewRentalHouse.objects.get(pk=id)
    hh_fobj = HouseHas.objects.filter(nrh=nrh_obj)
    a_fobj = Amenities.objects.filter(nrh=nrh_obj)
    r_fobj = Rules.objects.filter(nrh=nrh_obj)
    pt_fobj = PreferredTenant.objects.filter(nrh=nrh_obj)
    img_qset = HouseImages.objects.filter(nrh=nrh_obj)

    if request.method == 'GET':
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
        return render(request, 'renting/rental_ad_edit.html', locals())

    else:
        form = RentalHouseForm(
            initial={'country': 'Ghana'}, data=request.POST or None, instance=nrh_obj)
        images_list = []
        if img_qset:
            for img_obj in img_qset:
                images_list.append(img_obj)

        img_form = HouseImagesForm(
            request.POST or None, request.FILES or None, instance=img_obj)
        hform = HouseHasForm(request.POST or None, instance=hh_fobj[0])
        aform = AmenitiesForm(request.POST or None, instance=a_fobj[0])
        rform = RulesForm(request.POST or None, instance=r_fobj[0])
        ptform = PreferredTenantForm(request.POST or None, instance=pt_fobj[0])

        if request.method == 'POST':

            if all((form.is_valid(), hform.is_valid(), img_form.is_valid(), aform.is_valid(), rform.is_valid(), ptform.is_valid())):
                rh_obj = form.save(commit=False)
                rh_obj.user = request.user
                rh_obj.save()
                nrh_obj = NewRentalHouse.objects.get(pk=rh_obj.id)
                if img_form.is_valid():
                    for img_file in request.FILES.getlist('imagess'):
                        HouseImages.objects.create(
                            imagess=img_file, nrh=nrh_obj)
                    hs = hform.save(commit=False)
                    hs.nrh = nrh_obj
                    hs.save()
                    amf = aform.save(commit=False)
                    amf.nrh = nrh_obj
                    amf.save()
                    rf = rform.save(commit=False)
                    rf.nrh = nrh_obj
                    rf.save()
                    pf = ptform.save(commit=False)
                    pf.nrh = nrh_obj
                    pf.save()
                else:
                    print(img_form.errors)

                messages.success(
                    request, f'Your Ad has been Updated Successfully')
                return redirect('renting:landlordViewRentAds')


@user_passes_test(check_user, login_url='/signInLandlord')
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
        modl = 'true'
        return HttpResponseRedirect(reverse('renting:edit_whole', args=(id,)))


@user_passes_test(check_user, login_url='/signInLandlord')
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

        # Handle the error for house object which doesn't exists

    elif request.user.is_anonymous:
        modl = 'true'
        return render(request, 'renting/house_detail.html', locals())


@user_passes_test(check_user, login_url='/signInLandlord')
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
        modl = 'true'
        return render(request, 'renting/house_detail.html', locals())


@user_passes_test(check_user, login_url='/signInLandlord')
def del_house_image(request, id):
    if request.user.is_authenticated:
        if request.method == 'DELETE':
            try:
                img_obj = HouseImages.objects.get(pk=id)
            except:
                img_obj = None

            if img_obj:
                img_obj.delete()

                return JsonResponse({'object': 'deleted'})

            else:
                return JsonResponse({'object': 'not_found'}, status=404)


# the view for the first page of the nss accomodation.
def nssAccomFirstPage(request):
    return render(request, 'renting/index_NSS.html')


# the page for the landlord to register.
def registerAccount(request):
    form = StudentRegisterForm()
    user_contact_form = UserContactFrom()
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        user_contact_form = UserContactFrom(request.POST)
        if all((form.is_valid(), user_contact_form.is_valid())):

            tt = form.save()
            obs = user_contact_form.save(commit=False)
            obs.user_id_id = tt.id
            obs.save()

            return redirect('renting:signInLandlord')

    context = {
        'form': StudentRegisterForm(),
        'user_contact_form': UserContactFrom()
    }
    return render(request, 'renting/register.html', context)


# the sign in page for the landlord.
def signInLandlord(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:

            typed = Typed.objects.filter(user_id=user).first()
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
            Q(city__icontains=city_query)).distinct()

        context = {
            'house_list': house_list,
        }
        return render(request, 'renting/view_rent_adds.html', context)
    else:
        return render(request, 'renting/view_rent_adds.html')


# the page where a landlord can post his rent adds.
@user_passes_test(check_user, login_url='/signInLandlord')
def postRentAdds(request):
    form = RentalHouseForm(
        initial={'country': 'Ghana'}, data=request.POST or None)
    img_form = HouseImagesForm(request.POST, files=request.FILES)
    house_has_form = HouseHasForm(request.POST)
    amenities_form = AmenitiesForm(request.POST)
    rules_form = RulesForm(request.POST)
    preferred_tenant_form = PreferredTenantForm(request.POST)
    profile = Profile.objects.get(user_id=request.user.id)
    users_profile = Profile.objects.get(user_id=request.user.id)
    if users_profile.occupation == 'dummy_occupation':
        messages.success(
            request, f"Please update your profile!, Click on your username!")
        return redirect('renting:landlordProfile', id=request.user.id)

    if request.method == 'POST' and request.user.is_authenticated:

        if all((form.is_valid(), house_has_form.is_valid(), amenities_form.is_valid(), rules_form.is_valid(), preferred_tenant_form.is_valid())):
            rh_obj = form.save(commit=False)
            rh_obj.user = request.user
            rh_obj.landlord_profile = profile
            rh_obj.save()
            nrh_obj = NewRentalHouse.objects.get(pk=rh_obj.id)
            if img_form.is_valid():
                for img_file in request.FILES.getlist('imagess'):
                    HouseImages.objects.create(imagess=img_file, nrh=nrh_obj)
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

            messages.success(request, f'Your Ad has been Posted Successfully')
            return redirect('renting:postRentAdds')

    # GET Request
    elif request.user.is_anonymous:
        modl = 'true'
        return render(request, 'renting/post_rent_adds.html', locals())

    return render(request, 'renting/post_rent_adds.html', locals())


# check if student is authenticated
def check_student_user(user):
    if user.is_authenticated:
        typed = Typed.objects.filter(user_id=user).first()
        if typed.user_group == 'student':
            return user.first_name
    else:
        requesst = request
        return render(requesst, 'student/login_student.html')


# check if staff is authenticated
def check_staff_user(user):
    if user.is_authenticated:
        typed = Typed.objects.filter(user_id=user).first()
        if typed.user_group == 'staff':
            return user.first_name
    else:
        requesst = request
        return render(requesst, 'staff/login_staff.html')


# the page where a student can view all rent ads.
@user_passes_test(check_student_user, login_url='/loginStudent')
def studentViewRentAds(request):
    all_rental = NewRentalHouse.objects.all().order_by('-date_registered')

    f = SearchFilter(request.GET, queryset=all_rental)

    if f.qs.count() == 0:
        messages.info(request, f"No properties found")
        return render(request, 'renting/student_view_rent_ads.html', {'filter': all_rental})
    else:
        return render(request, 'renting/student_view_rent_ads.html', {'filter': f.qs})

# the page where a staff can view all rent ads.


@user_passes_test(check_staff_user, login_url='/loginStaff')
def staffViewRentAds(request):
    all_rental = NewRentalHouse.objects.all()

    f = SearchFilter(request.GET, queryset=all_rental)

    if f.qs.count() == 0:
        messages.info(request, f"No properties found")
        return render(request, 'renting/staff_view_rent_ads.html', {'filter': all_rental})
    else:
        return render(request, 'renting/staff_view_rent_ads.html', {'filter': f.qs})


# the page where a landlord can view all of their posted ads.
@user_passes_test(check_user, login_url='/signInLandlord')
def landlordViewRentAds(request):
    all_rental = NewRentalHouse.objects.filter(
        user=request.user).order_by('-date_registered')

    f = SearchFilter(request.GET, queryset=all_rental)

    if f.qs.count() == 0:
        messages.info(request, f"No properties found")
        return render(request, 'renting/landlord_view_rent_ads.html', {'filter': all_rental})
    else:
        return render(request, 'renting/landlord_view_rent_ads.html', {'filter': f.qs})


# landlord delete rent ad
@user_passes_test(check_user, login_url='/signInLandlord')
def delete_rent_ad(request, id):
    product = get_object_or_404(NewRentalHouse, pk=id)
    house_list = NewRentalHouse.objects.filter(
        user=request.user).order_by('-date_registered')
    if request.method == 'POST':
        product.delete()
        return redirect('renting:landlordViewRentAds')
    return render(request, 'renting/delete_form.html', locals())


# the page where the landlord can see his own house details.
@user_passes_test(check_user, login_url='/signInLandlord')
def landlordViewHouseDetails(request, id):
    if request.user.is_authenticated:
        try:
            nrh_obj = NewRentalHouse.objects.get(pk=id)
            r_hh = HouseHas.objects.get(nrh=nrh_obj)
            am = Amenities.objects.get(nrh=nrh_obj)
            pt = PreferredTenant.objects.get(nrh=nrh_obj)
            rl = Rules.objects.get(nrh=nrh_obj)
            imgs = HouseImages.objects.filter(nrh=nrh_obj)
            rating_count = Rating.objects.filter(
                landlord_id=nrh_obj.id).count()
            rating = Rating.objects.filter(
                landlord_id=nrh_obj.id).order_by('-date')
            print(rating_count)
            for img in imgs:
                print(img.images)
        except:
            nrh_obj = None
        if nrh_obj:
            return render(request, 'renting/landlord_view_own_ads_details.html', locals())
    elif request.user.is_anonymous:
        modl = 'true'
        return render(request, 'renting/landlord_view_own_ads_details.html', locals())


# the page where the student can view the details of the ad.
@user_passes_test(check_student_user, login_url='/loginStudent')
def studentViewHouseDetails(request, id):
    form = RatingForm(request.POST)

    product = get_object_or_404(NewRentalHouse, pk=id)
    if request.method == "POST":
        nrh_obj = NewRentalHouse.objects.get(pk=id)
        r_hh = HouseHas.objects.get(nrh=nrh_obj)
        am = Amenities.objects.get(nrh=nrh_obj)
        pt = PreferredTenant.objects.get(nrh=nrh_obj)
        rl = Rules.objects.get(nrh=nrh_obj)
        imgs = HouseImages.objects.filter(nrh=nrh_obj)
        rating_count = Rating.objects.filter(landlord_id=nrh_obj.id).count()
        rating = Rating.objects.filter(
            landlord_id=nrh_obj.id).order_by('-date')
        for img in imgs:
            print(img.images)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.user = request.user
            fm.landlord = product
            fm.save()

        return render(request, 'renting/student_view_ad_details.html', locals())

    if request.user.is_authenticated:
        try:
            nrh_obj = NewRentalHouse.objects.get(pk=id)
            city = nrh_obj.city
            recommendation = NewRentalHouse.objects.filter(city=city).exclude(pk=id)
            imgee = HouseImages.objects.filter(nrh=recommendation)
            r_hh = HouseHas.objects.get(nrh=nrh_obj)
            am = Amenities.objects.get(nrh=nrh_obj)
            pt = PreferredTenant.objects.get(nrh=nrh_obj)
            rl = Rules.objects.get(nrh=nrh_obj)
            imgs = HouseImages.objects.filter(nrh=nrh_obj)
            rating_count = Rating.objects.filter(landlord_id=nrh_obj.id).count()
            rating = Rating.objects.filter(landlord_id=nrh_obj.id).order_by('-date')
            for img in imgs:
                print(img.images)
        except:
            nrh_obj = None
        if nrh_obj:
            return render(request, 'renting/student_view_ad_details.html', locals())
    elif request.user.is_anonymous:
        modl = 'true'
        return render(request, 'renting/student_view_ad_details.html', locals())


# the page where the student can view the details of the landlord.


@user_passes_test(check_student_user, login_url='/loginStudent')
def studentViewLandlordDetails(request, id):
    landlord = User.objects.get(id=id)
    profile = Profile.objects.get(user_id=id)
    typed = Typed.objects.get(user_id_id=id)

    contact_landlord = ContactLandlordForm(request.POST)
    if request.method == 'POST':
        if contact_landlord.is_valid():
            cl = contact_landlord.save(commit=False)
            cl.user = request.user
            cl.landlord_id = request.user.id
            cl.save()

            return render(request, 'renting/student_view_landlord_details.html')
    context = {
        'landlord': landlord,
        'profile': profile,
        'typed': typed,
    }
    return render(request, 'renting/student_view_landlord_details.html', context)


# the page where the staff can view the details of the landlord.
@user_passes_test(check_staff_user, login_url='/loginStaff')
def staffViewLandlordDetails(request, id):
    landlord = User.objects.get(id=id)
    profile = Profile.objects.get(user_id=id)
    typed = Typed.objects.get(user_id_id=id)
    contact_landlord = ContactLandlordForm(request.POST)
    # print(contact_landlord)
    if request.method == 'POST':
        print(contact_landlord)
        if contact_landlord.is_valid():
            cl = contact_landlord.save(commit=False)
            print(cl)
            cl.user = request.user
            cl.landlord_id = request.user.id
            cl.save()

            return render(request, 'renting/staff_view_landlord_details.html')

    context = {
        'landlord': landlord,
        'profile': profile,
        'typed': typed,
    }

    return render(request, 'renting/staff_view_landlord_details.html', context)

# Landlor view details of other landlords


@user_passes_test(check_user, login_url='/signInLandlord')
def landlordViewLandlordDetails(request, id):
    landlord = User.objects.get(id=id)
    profile = Profile.objects.get(user_id=id)
    typed = Typed.objects.get(user_id_id=id)
    pp = Profile.objects.get(user_id=31)

    contact_landlord = ContactLandlordForm(request.POST)
    if request.method == 'POST':
        if contact_landlord.is_valid():
            cl = contact_landlord.save(commit=False)
            cl.user = request.user
            cl.landlord_id = request.user.id
            cl.save()

            return render(request, 'renting/landlord_view_landlord_details.html')
    context = {
        'landlord': landlord,
        'profile': profile,
        'typed': typed,
    }
    return render(request, 'renting/landlord_view_landlord_details.html', context)


# the page where the staff can view the details of the ad.
@user_passes_test(check_staff_user, login_url='/loginStaff')
def staffViewAdDetails(request, id):
    form = RatingForm(request.POST)
    product = get_object_or_404(NewRentalHouse, pk=id)
    if request.method == "POST":
        nrh_obj = NewRentalHouse.objects.get(pk=id)
        r_hh = HouseHas.objects.get(nrh=nrh_obj)
        am = Amenities.objects.get(nrh=nrh_obj)
        pt = PreferredTenant.objects.get(nrh=nrh_obj)
        rl = Rules.objects.get(nrh=nrh_obj)
        imgs = HouseImages.objects.filter(nrh=nrh_obj)
        rating_count = Rating.objects.filter(landlord_id=nrh_obj.id).count()
        rating = Rating.objects.filter(
            landlord_id=nrh_obj.id).order_by('-date')
        for img in imgs:
            print(img.images)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.user = request.user
            fm.landlord = product
            fm.save()

        return render(request, 'renting/staff_view_ad_details.html', locals())

    if request.user.is_authenticated:
        try:
            nrh_obj = NewRentalHouse.objects.get(pk=id)
            r_hh = HouseHas.objects.get(nrh=nrh_obj)
            am = Amenities.objects.get(nrh=nrh_obj)
            pt = PreferredTenant.objects.get(nrh=nrh_obj)
            rl = Rules.objects.get(nrh=nrh_obj)
            imgs = HouseImages.objects.filter(nrh=nrh_obj)
            rating_count = Rating.objects.filter(
                landlord_id=nrh_obj.id).count()
            rating = Rating.objects.filter(
                landlord_id=nrh_obj.id).order_by('-date')
            for img in imgs:
                print(img.images)
        except:
            nrh_obj = None
        if nrh_obj:
            return render(request, 'renting/staff_view_ad_details.html', locals())
    elif request.user.is_anonymous:
        modl = 'true'
        return render(request, 'renting/staff_view_ad_details.html', locals())


# the landlord profile page.


@user_passes_test(check_user, login_url='/signInLandlord')
def landlordProfile(request, id):
    profile = Profile.objects.get(user_id=request.user.id)
    profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
    if request.method == 'GET':
        context = {
            'profile': profile,
            'profile_form': ProfileForm(instance=profile)
        }
        return render(request, 'renting/landlord_profile.html', context)

    elif request.method == 'POST':
        if profile_form.is_valid():
            pro = profile_form.save(commit=False)
            pro.user_id = request.user.id
            pro.save()
            messages.success(request, f'Your profile has been Updated!')
            return redirect('renting:landlordViewRentAds')

    context = {
        'profile_form': profile_form
    }
    return render(request, 'renting/landlord_profile.html', context)


# Payment Process for Student


def student_payment(request):
    form = PaymentsForm(request.POST)
    if request.method == 'POST':
        print(request.POST)
        pay_form = PaymentsForm(request.POST, request.FILES)

        if pay_form.is_valid():
            obj = pay_form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(
                request, f'Your Payment has been Updated Successfully')
            return redirect('renting:studentViewRentAds')
    else:
        context = {
            'form': PaymentsForm(),
        }
        return render(request, "renting/student_payment.html", context)


# Process Payment for Staff
def staff_payment(request):
    form = PaymentsForm(request.POST)
    if request.method == 'POST':
        print(request.POST)
        pay_form = PaymentsForm(request.POST, request.FILES)

        if pay_form.is_valid():
            obj = pay_form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(
                request, f'Your Payment has been Updated Successfully')
            return redirect('renting:staffViewRentAds')
    else:
        context = {
            'form': PaymentsForm(),
        }
        return render(request, "renting/staff_payment.html", context)


# landlord view ads from other landlords.
@user_passes_test(check_user, login_url='/signInLandlord')
def landlordViewAdsOfOtherLandlords(request):
    all_rental = NewRentalHouse.objects.exclude(
        user_id=request.user).order_by('-date_registered')

    f = SearchFilter(request.GET, queryset=all_rental)

    if f.qs.count() == 0:
        messages.info(request, f"No properties found")
        return render(request, 'renting/landlord_view_other_landlord_houses.html', {'filter': all_rental})
    else:
        return render(request, 'renting/landlord_view_other_landlord_houses.html', {'filter': f.qs})

# landlord view details of ads posted by other landlords


@user_passes_test(check_user, login_url='/signInLandlord')
def landlordViewAdsDetailsOfOtherLandlords(request, id):
    form = RatingForm(request.POST)
    product = get_object_or_404(NewRentalHouse, pk=id)
    if request.method == "POST":
        nrh_obj = NewRentalHouse.objects.get(pk=id)
        r_hh = HouseHas.objects.get(nrh=nrh_obj)
        am = Amenities.objects.get(nrh=nrh_obj)
        pt = PreferredTenant.objects.get(nrh=nrh_obj)
        rl = Rules.objects.get(nrh=nrh_obj)
        imgs = HouseImages.objects.filter(nrh=nrh_obj)
        rating_count = Rating.objects.filter(landlord_id=nrh_obj.id).count()
        rating = Rating.objects.filter(
            landlord_id=nrh_obj.id).order_by('-date')
        for img in imgs:
            print(img.images)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.user = request.user
            fm.landlord = product
            fm.save()

        return render(request, 'renting/landlord_view_details_of_ads_posted_by_other_landlords.html', locals())

    if request.user.is_authenticated:
        try:
            nrh_obj = NewRentalHouse.objects.get(pk=id)
            r_hh = HouseHas.objects.get(nrh=nrh_obj)
            am = Amenities.objects.get(nrh=nrh_obj)
            pt = PreferredTenant.objects.get(nrh=nrh_obj)
            rl = Rules.objects.get(nrh=nrh_obj)
            imgs = HouseImages.objects.filter(nrh=nrh_obj)
            rating_count = Rating.objects.filter(
                landlord_id=nrh_obj.id).count()
            rating = Rating.objects.filter(
                landlord_id=nrh_obj.id).order_by('-date')
            for img in imgs:
                print(img.images)
        except:
            nrh_obj = None
        if nrh_obj:
            return render(request, 'renting/landlord_view_details_of_ads_posted_by_other_landlords.html', locals())
    elif request.user.is_anonymous:
        modl = 'true'
        return render(request, 'renting/landlord_view_details_of_ads_posted_by_other_landlords.html', locals())
    return render(request, 'renting/landlord_view_details_of_ads_posted_by_other_landlords.html')


# landlord edit rent ads
@user_passes_test(check_user, login_url='/signInLandlord')
def landlordEditRentAds(request):
    return render(request, 'renting/landlord_edit_rent_ads.html')
