from django.urls import path
from tracking import views as tr



app_name='tracking'
urlpatterns = [
	path('', tr.index, name='index'),
	path('loginStudent/', tr.loginStudent, name='loginStudent'),
	path('loginStaff/', tr.loginStaff, name='loginStaff'),
	path('studentSignUp/', tr.studentSignUp, name='studentSignUp'),
	path('studentDashboard/', tr.studentDashboard, name='studentDashboard'),
	path('studentSubmitComplaint/', tr.studentSubmitComplaint, name='studentSubmitComplaint'),
	path('studentViewAllComplaints/', tr.studentViewAllComplaints, name='studentViewAllComplaints'),
	path('studentViewAnnouncements/', tr.studentViewAnnouncements, name='studentViewAnnouncements'),
	path('staffDashboard/', tr.staffDashboard, name='staffDashboard'),
	path('addNewStudent/', tr.addNewStudent, name='addNewStudent'),
	path('addNewVisitor/', tr.addNewVisitor, name='addNewVisitor'),
	path('postAnnouncement/', tr.postAnnouncement, name='postAnnouncement'),

	
]

