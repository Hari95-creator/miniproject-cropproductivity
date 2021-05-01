import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from cropapp.models import admin
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
                return render(request,'user/signup.html',{'msg':'username already exist'})
            elif uphone == x.phone:
                return render(request,'user/signup.html',{'msg':'phonenumber already exist'})
            elif e_mail == x.email:
                return render(request,'user/signup.html',{'msg':'email already exist'})
            else:
                pass
        
        myobj=userregister(fname=first_name,lname=last_name,uname=user_name,pwd=pass_word,email=e_mail,phone=uphone)
        myobj.save()
        
    return render(request,'user/signup.html')

def user_details(request):
    adminobj=userregister.objects.all()
    return render(request, 'admin/userdetails.html', {'farmers': adminobj})

def login(request):
    if request.method== 'POST':

        utype = request.POST.get('utype')
        uname = request.POST.get('user_name')
        pwd = request.POST.get('pass_word')

        if utype =='uadmin':
        
            try:
                if admin.objects.get(uname=uname) is not None:
                
                    ad=admin.objects.get(uname=uname)
                
                    if pwd ==ad.pwd:
                    
                        request.session['sessionid']= ad.uname
                        request.session['password'] = ad.pwd
                       
                        return HttpResponse('Admin Login success')
                    
                    else:
                        
                        return render(request,'login.html',{'status':'Wrong Admin Password Try Again ....'})

            except:

                    return render(request,'login.html',{'status':"Oops Admin not in our database ...."})
        else:

            try:

                if userregister.objects.get(uname=uname) is not None:

                    user1=userregister.objects.get(uname=uname)

                    if pwd== user1.pwd:

                        request.session['sessionid']=user1.uname
                        request.session['upassword']=user1.pwd
                        
                        return HttpResponse('User login success')
                    
                    else:

                        return render(request,'login.html',{'status':'Wrong User Password Try Again ....'})
            
            except:
                
                return render(request,'login.html',{'status':'Oops User not in our database ....'})

    return render(request,'login.html')
    

def soiltest(request):
    return render(request,'user/soiiltest.html',)

def soilPredictionDb(request):
    data=pd.read_csv("media/data/predictData.csv")
    croplist=["coconut","Mango","Jackfruit","Onion",]
    print(data)
    x=data.iloc[:,[0,1,2,3,4,5,6,7,8]].values
    print(x)
    y=data['class']
    print(y)
    from sklearn.model_selection import train_test_split
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=2)
    knn=DecisionTreeClassifier()
    print(knn.fit(x_train,y_train))
    x0=float(request.POST.get('ca'))
    x1=float(request.POST.get('mag'))
    x2=float(request.POST.get('po'))
    x3=float(request.POST.get('sul'))
    x4=float(request.POST.get('nit'))
    x5=float(request.POST.get('lime'))
    x6=float(request.POST.get('carb'))
    x7=float(request.POST.get('ph'))
    x8=float(request.POST.get('moist'))
    y_pred=knn.predict([[x0,x1,x2,x3,x4,x5,x6,x7,x8]])
    print(y_pred,"type=",type(y_pred))
    nn=int(y_pred)-1
    print("NNN=",nn)
    result=croplist[nn]
    print("result=",result)
    user=userregister.objects.get(id=request.POST.get('uid'))
    db=soilPrediction(uid=user,cal=x0,mag=x1,po=x2,sul=x3,nit=x4,lim=x5,carb=x6,phos=x7,moist=x8,result=result)
    db.save()

    user=userdata(request)
    print(result)
    return render(request,'user/soiiltest.html',{'user':user,'result':result})
    










#this for testing purpose function
def testing(request):
#     testobj=userregister.objects.all()
#     return render(request,'admin/test.html',{'testing':testobj})
    return render(request,'admin/test.html')


 

