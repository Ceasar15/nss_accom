from django.shortcuts import render
from django.contrib.auth import logout




# Create your views here.
def index(request):
    return render(request, 'tracking/indexxxx.html')




# The about page.
def about(request):
    return render(request, 'tracking/about.html')



# The frequently asked questions page.
def faq(request):
    return render(request, 'tracking/faq.html')





