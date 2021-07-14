from django.urls import path
from staff import models as sf

app_name = 'staff'

urlpatterns = [
    
    path('loginStudent/', sf.loginStudent, name='loginStudent'),    
    #path('studentDashboard/', sf.studentDashboard, name='studentDashboard'),
]
