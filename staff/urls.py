from django.urls import path
from staff import views as sf

app_name = 'staff'

urlpatterns = [
    
    path('loginStaff/', sf.loginStaff, name='loginStaff'),    
    path('addNewStudent/', sf.staff_addNewStudent, name='addNewStudent'),
    path('addNewVisitor/', sf.staff_addNewVisitor, name='addNewVisitor'),
    path('staffDashboard/', sf.staffDashboard, name='staffDashboard'),
<<<<<<< HEAD
    path('postAnnouncement/', sf.staff_postAnnouncement, name='postAnnouncement'),
||||||| ed5ec9d
    path('staffDashboard/', sf.staffDashboard, name='staffDashboard'),
=======
    path('postAnnouncement/', sf.staff_postAnnouncement, name='staff_postAnnouncement'),
>>>>>>> 267ab626ae90cefc7d1800b7691d4e1fd8114605
]
