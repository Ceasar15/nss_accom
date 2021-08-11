from django.urls import path
from renting import views as rt
from users import views as us


app_name='renting'
urlpatterns = [
    path('disp/', rt.search_list, name='disp'),
    path('update_ad/<int:id>/', rt.update_rent_ad, name='update_rent_ad'),
    path('edw/<int:id>/', rt.edit_whole, name='edit_whole'),
    path('dlw/<int:id>/', rt.delete_whole, name='del_whole'),
    path('hd/<int:id>/', rt.house_details, name='house_details'),
    path('adlist/', rt.rent_ads, name='rent_ad_list'),
    path('del_img/<int:id>/',rt.del_house_image, name='del_img'),
    path('nssAccomFirstPage/', rt.nssAccomFirstPage, name='nssAccomFirstPage'),
    path('registerAccount/', rt.registerAccount, name='registerAccount'),
    path('signInLandlord/', rt.signInLandlord, name='signInLandlord'),
    path('viewRentAdds/', rt.viewRentAdds, name='viewRentAdds'),
    path('postRentAdds/', rt.postRentAdds, name='postRentAdds'),
    path('landlord_register/', us.LandlordRegister, name='loginLandlord'),
    path('landlordViewRentAds', rt.landlordViewRentAds, name='landlordViewRentAds'),
    path('studentViewRentAds/', rt.studentViewRentAds, name='studentViewRentAds'),
    path('studentViewHouseDetails/<int:id>/', rt.studentViewHouseDetails, name='studentViewHouseDetails'),
    path('studentViewLandlordDetails/<int:id>/', rt.studentViewLandlordDetails, name='studentViewLandlordDetails'),
    path('staffViewRentAds/', rt.staffViewRentAds, name='staffViewRentAds'),
    path('staffViewAdDetails/<int:id>/', rt.staffViewAdDetails, name='staffViewAdDetails'),
    path('staffViewLandlordDetails/<int:id>/', rt.staffViewLandlordDetails, name='staffViewLandlordDetails'),
    path('landlordViewHouseDetails/<int:id>/', rt.landlordViewHouseDetails, name='landlordViewHouseDetails'),
    path('landlordProfile/<int:id>', rt.landlordProfile, name='landlordProfile'),
    path('update_profile/<int:id>', rt.update_landlordProfile, name='update_profile'),
    path('student_payment/', rt.student_payment, name="student_payment"),
    path('staff_payment/', rt.staff_payment, name="staff_payment"),
    path('landlordViewAdsOfOtherLandlords/', rt.landlordViewAdsOfOtherLandlords, name='landlordViewAdsOfOtherLandlords')

]