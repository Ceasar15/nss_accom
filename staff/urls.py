from django.urls import path
from staff import models as sf

app_name = 'staff'

urlpatterns = [
    
    path('loginStaff/', sf.loginSaff, name='loginStaff'),    
    #path('studentDashboard/', sf.studentDashboard, name='studentDashboard'),
]
