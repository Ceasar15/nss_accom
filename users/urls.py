from django.urls import path, include


from users.views import user_type, settings, account_delete
from users import views 
from django.contrib.auth.views import LoginView



app_name = 'users'
urlpatterns = [
	path('type/',user_type, name='type'),
	path('acc/',settings, name='settings'),
	path('del/',account_delete, name='del_acc'),
    path('student_register/', views.Studentregister, name='student_register'),
    path('staff_register/', views.StaffRegister, name='staff_register'),
    path('staff_register/', views.Staffregister, name='staff_register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password-change/', views.password_change, name='password_change'),
    path('logout/', views.logout_view, name='logout'),
    path('welcome/', views.welcome, name='welcome'),
]