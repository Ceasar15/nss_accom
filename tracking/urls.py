from django.urls import path
from tracking import views as tr



app_name='tracking'
urlpatterns = [
	path('', tr.index, name='index'),
]
