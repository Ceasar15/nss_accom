from django.urls import path
from student import views as st

from distutils.version import StrictVersion  # pylint: disable=no-name-in-module,import-error
from django import get_version

if StrictVersion(get_version()) >= StrictVersion('2.0'):
    from django.urls import re_path as pattern
else:
    from django.conf.urls import url as pattern


app_name = 'student'

urlpatterns = [
    path('loginStudent/', st.loginStudent, name='loginStudent'),
    path('studentDashboard/', st.studentDashboard, name='studentDashboard'),
	path('studentSubmitComplaint/', st.studentSubmitComplaint, name='studentSubmitComplaint'),
	path('studentViewAllComplaints/', st.studentViewAllComplaints, name='studentViewAllComplaints'),
	path('studentViewAnnouncements/', st.studentViewAnnouncements, name='studentViewAnnouncements'),
	pattern('mark-all-as-read/$', st.mark_all_as_read, name='mark_all_as_read'),
    pattern('mark-as-read/(?P<slug>\d+)/$', st.mark_as_read, name='mark_as_read'),

]
