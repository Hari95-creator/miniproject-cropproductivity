from cropapp.models import userregister
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
def  index(request):
    return render(request,'index.html')
def  adminbase(request):
    return render(request,'admin/adminbasee.html')
def  userbase(request):
    return render(request,'user/userbase.html')

def  signup(request):
    
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        user_name=request.POST.get('user_name')
        pass_word=request.POST.get('pass_word')
        e_mail=request.POST.get('email')
        uphone=request.POST.get('phone')
        newobj=userregister.objects.all()
        
        for x in newobj:
            if user_name == x.uname:
                return HttpResponse('username already exist')
            elif uphone == x.phone:
                return HttpResponse('phonenumber already exist')
            elif e_mail == x.email:
                return HttpResponse('email already exist')
            else:
                pass
        
        myobj=userregister(fname=first_name,lname=last_name,uname=user_name,pwd=pass_word,email=e_mail,phone=uphone)
        myobj.save()
        
    return render(request,'user/signup.html')

def user_details(request):
    adminobj=userregister.objects.all()
    return render(request, 'admin/userdetails.html', {'farmers': adminobj})

def testing(request):
    testobj=userregister.objects.all()
    return render(request,'admin/test.html',{'testing':testobj})


 

