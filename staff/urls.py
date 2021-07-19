from django.urls import path
from staff import views as sf

app_name = 'staff'

urlpatterns = [
    
    path('loginStaff/', sf.loginStaff, name='loginStaff'),   
    path('addNewStudent/', sf.staff_addNewStudent, name='addNewStudent'),
    path('addNewVisitor/', sf.staff_addNewVisitor, name='addNewVisitor'),
    path('staffDashboard/', sf.staffDashboard, name='staffDashboard'),
    path('staffUpdateVisitor/', sf.updateVisitorStatus, name='updateVisitor'),
    path('staffPostAnnouncement/', sf.staffPostAnnouncement, name='staffPostAnnouncement')
]
