from django.urls import path
from staff import views as sf

app_name = 'staff'

urlpatterns = [
    
    path('loginStaff/', sf.loginStaff, name='loginStaff'),    
    path('staffDashboard/', sf.staffDashboard, name='staffDashboard'),
]
