from django.urls import path
from student import views as st

app_name = 'student'

urlpatterns = [
    path('loginStudent/', st.loginStudent, name='loginStudent'),    
    path('studentDashboard/', st.studentDashboard, name='studentDashboard'),
	path('studentSubmitComplaint/', st.studentSubmitComplaint, name='studentSubmitComplaint'),
	path('studentViewAllComplaints/', st.studentViewAllComplaints, name='studentViewAllComplaints'),
	path('studentViewAnnouncements/', st.studentViewAnnouncements, name='studentViewAnnouncements')
]
