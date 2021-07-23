from django.urls import path
from staff import views as sf

app_name = 'staff'


urlpatterns = [
    
    path('loginStaff/', sf.loginStaff, name='loginStaff'),   
    path('addNewStudent/', sf.staff_addNewStudent, name='addNewStudent'),
    path('addNewVisitor/', sf.staff_addNewVisitor, name='addNewVisitor'),
    path('list_viewVisitor/', sf.list_viewVisitor, name='list_viewVisitor'),
    path('<vistoor_id>/update_viewVisitor/', sf.update_viewVisitor, name='update_viewVisitor'),
    path('v/<vistor_id>/', sf.detail_viewVisitor, name='detail_viewVisitor'),
    path('staffDashboard/', sf.staffDashboard, name='staffDashboard'),
    path('staffUpdateVisitor/', sf.updateVisitorStatus, name='updateVisitor'),
    path('staffPostAnnouncement/', sf.staffPostAnnouncement, name='staffPostAnnouncement'),
    path('staffViewAllStudents/', sf.staffViewAllStudents, name='staffViewAllStudents'),
    path('staffManageVisitors/', sf.staffManageVisitors, name='staffManageVisitors'),
    path('staffViewAllComplaints/', sf.staffViewAllComplaints, name='staffViewAllComplaints'),
    path('leave/<vistor_id>', sf.leave, name='leave'),
    path('solved/<complaint_id>', sf.solved, name='solved'),
    path('check_in/<id>', sf.check_in, name='check_in'),
]
