from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url 
from django.contrib.auth.views import LogoutView
import notifications.urls

urlpatterns = [

	path('admin/doc/',include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include('student.urls')),
    path('', include('staff.urls')),
    path('', include('tracking.urls')),
    path('', include('renting.urls')),
    path('',include('social_django.urls', namespace='social')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('usr/',include('users.urls')),
    path('logout/', LogoutView.as_view(), name='logout')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
