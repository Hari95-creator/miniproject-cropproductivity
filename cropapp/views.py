from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
def  index(request):
    return render(request,'index.html')
def  adminbase(request):
    return render(request,'admin/adminbasee.html')
def  userbase(request):
    return render(request,'user/userbase.html')
def  signup(request):
    return render(request,'user/signup.html')

