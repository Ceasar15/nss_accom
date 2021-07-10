from django.urls import path
from tracking import views as tr


app_name='tracking'
urlpatterns = [
	path('', tr.index, name='index'),
	path('loginStudent/', tr.loginStudent, name='loginStudent'),
	path('loginStaff/', tr.loginStaff, name='loginStaff'),
	path('studentSubmitComplaint/', tr.studentSubmitComplaint, name='studentSubmitComplaint')
]