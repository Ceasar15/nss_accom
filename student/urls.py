from django.urls import path
from django.contrib.auth.views import LoginView
from student import views as st

app_name = 'student'

urlpatterns = [
    path('loginStudent/', st.loginStudent, name='loginStudent'),
	path('studentSignUp/', st.studentSignUp, name='studentSignUp'),
	# path('login/', LoginView.as_view(template_name='tracking/login.html'), name='login'),
    path('studentDashboard/', st.studentDashboard, name='studentDashboard'),
	path('studentSubmitComplaint/', st.studentSubmitComplaint, name='studentSubmitComplaint'),
	path('studentViewAllComplaints/', st.studentViewAllComplaints, name='studentViewAllComplaints'),
	path('studentViewAnnouncements/', st.studentViewAnnouncements, name='studentViewAnnouncements')
]
