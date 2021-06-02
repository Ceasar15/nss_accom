from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),






    # path('', include('main.urls')),  # Added url pattern for main app
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('payment/', include('payment.urls')),
    # path('reserve/', include('reserve.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
