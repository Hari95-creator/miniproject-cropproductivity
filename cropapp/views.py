import pandas as pd
import datetime
from sklearn.tree import DecisionTreeClassifier
from cropapp.models import admin
from cropapp.models import userregister,soilPrediction,weatherPrediction,crops,account,orders
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Create your views here.

def  index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def aboutuser(request):
    user=userdata(request)
    return render(request,'user/about.html',{'user':user})

def aboutadmin(request):
    admin=admindata(request)
    return render(request,'admin/about.html',{'admin':admin})

def contactuser(request):
    user=userdata(request)
    return render(request,'user/contact.html',{'user':user})

def contactadmin(request):
    admin=admindata(request)
    return render(request,'user/contact.html',{'admin':admin})

def contact(request):
    return render(request,'contact.html')

def productview(request):
    user=userdata(request)
    view=crops.objects.get(pid=request.POST.get("proid"))
    print(view.pid)
    return render(request,'user/productview.html',{'user':user,'view':view})

def userdata(request):
    try:
        if request.session.has_key('sessionid'):
            
            udata=userregister.objects.get(uname=request.session['sessionid'])
            return udata

        else:

            return index(request)

    except:
    
        return index(request)

def admindata(request):
    try:
        if request.session.has_key('sessionid'):
            
            udata=admin.objects.get(uname=request.session['sessionid'])
            return udata

        else:

            return index(request)

    except:
    
        return index(request)

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
    admin=admindata(request)
    adminobj=userregister.objects.all()
    return render(request, 'admin/userdetails.html', {'farmers': adminobj,'admin':admin})

def userhome(request):
    user=userdata(request)
    cropview=crops.objects.all()
    return render(request,'user/userhome.html',{'user':user,'cropview':cropview})

def adminhome(request):
    admin=admindata(request)
    return render(request,'admin/adminhome.html',{'admin':admin})

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
                       
                        return adminhome(request)
                    
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
                        
                        return userhome(request)
                    
                    else:

                        return render(request,'login.html',{'status':'Wrong User Password Try Again ....'})
            
            except Exception as e:
                print(e)
                return render(request,'login.html',{'status':'Oops User not in our database ....'})

    return render(request,'login.html')



def soiltest(request):
    # user=userregister.objects.get(uname=request.session('sessionid'))
    user=userdata(request)
    # return render(request,'user/soiiltest.html')
    return render(request,'user/soiiltest.html',{'user':user})

def soilPredictionDb(request):
    data=pd.read_csv("media/data/predictData.csv")
    croplist=["coconut","Mango","Jackfruit","Onion","cumcumber"]
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
    # user=userregister.objects.get(id=1)
    user = userregister.objects.get(id=request.POST.get('uid'))
    db=soilPrediction(uid=user,cal=x0,mag=x1,po=x2,sul=x3,nit=x4,lim=x5,carb=x6,phos=x7,moist=x8,result=result)
    db.save()

    user=userdata(request)
    print(result)
    # return render(request,'user/soiiltest.html',{'result':result})
    return render(request,'user/soiiltest.html',{'user':user,'result':result})


def weathertest(request):
    user=userdata(request)
    print (user.id)
    # return render(request,'user/weathertest.html')
    return render(request,'user/weathertest.html',{'user':user})

def weatherPredictionDb(request):

    crops = ['wheat', 'mungbean', 'Tea', 'millet', 'maize', 'lentil', 'jute', 'cofee', 'cotton', 'ground nut', 'peas',
             'rubber', 'sugarcane', 'tobacco', 'kidney beans', 'moth beans', 'coconut', 'blackgram', 'adzuki beans',
             'pigeon peas', 'chick peas', 'banana', 'grapes', 'apple', 'mango', 'muskmelon', 'orange', 'papaya',
             'watermelon', 'pomegranate']

    data = pd.read_csv('media/data/weather.csv')
    print(data.head(1))
    # Creating dummy variable for target i.e label
    print('The data present in one row of the dataset is')
    print(data.head(1))
    y = data[['label']]
    x = data[['temperature', 'humidity', 'ph', 'rainfall']]
    # Dividing the data into training and test set

    # Importing Decision Tree classifier
    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier()
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=2)
    # Fitting the classifier into training set
    clf.fit(x_train, y_train)
    x1 = float(request.POST.get('temp'))
    x2 = float(request.POST.get('hum'))
    x3 = float(request.POST.get('ph'))
    x4 = float(request.POST.get('rain'))
    predicted = clf.predict([[x1, x2, x3, x4]])
    print(predicted)
    nn = int(predicted)
    result = crops[nn]
    # user = userregister.objects.get(id=1)
    user = userregister.objects.get(id=request.POST.get('uid'))
    db = weatherPrediction(uid=user, temp=x1, hum=x2, ph=x3, rain=x4, result=result)
    db.save()
    user = userdata(request)
    return render(request,'user/weathertest.html',{'user':user,'result':result})
    # return render(request, 'user/weathertest.html', {'result': result})

def addproduct(request):
    admin=admindata(request)
    return render(request,'admin/addproduct.html',{'admin':admin})

def addItemdb(request):

    if request.method=='POST' and request.FILES['pic']:
        uploaded_file=request.FILES['pic']
        fs=FileSystemStorage()
        fname=uploaded_file.name
        filename=fs.save(fname,uploaded_file)
        uploaded_file_url=fs.url(filename)
        db=crops(pname=request.POST.get('pname'),price=request.POST.get('price'),img=uploaded_file_url,desc=request.POST.get('desc'),)
        db.save()
    return adminhome(request)

def order(request):
    return render(request,'user/order.html')

def buynow(request):
    user=userdata(request)
    print(request.POST.get("proid"))
    product=crops.objects.get(pid=request.POST.get("proid"))
    total=float(request.POST.get('q1'))*float(product.price)
    print('test',request.POST.get('q1'))
    print('price:',product.price)
    print("test1")
    print('total:',total)
    # print(request.POST.get("proid"))
    return render(request,'user/buynow.html',{'pro':product,'total':total,'q1':request.POST.get('q1')})

def manage_account(request):
    return render(request,'user/account.html')

def userAddMoney(request):
    try:
            db = account.objects.get(cardnum=request.POST.get('cnum'))
            print(db.cardnum)
            if db.cvv == request.POST.get('cvv') :
                    print("same exp")
                    db.bal += int(request.POST.get('amnt'))
                    db.save()
                    return manage_account(request)

            else:
                return HttpResponse("Exp or cvv incorrect")
    except:
        print(request.POST.get("edate"))
        db = account(cardnum=request.POST.get('cnum'), cvv=request.POST.get('cvv'),bal=request.POST.get('amnt'),expdate=request.POST.get('edate'))
        db.save()
        return manage_account(request)

def placeOrder(request):
    udata = userdata(request)
    tamount = float(request.POST.get('total'))
    print("total==", tamount)
    if account.objects.get(cardnum=request.POST.get('card')) is not None:
        pay = account.objects.get(cardnum=request.POST.get('card'))
        if pay.cvv != request.POST.get('cvv'):
            return HttpResponse("incorrect CVV")
        else:
            print("tamountss==", tamount)
            if float(pay.bal) < tamount:
                return HttpResponse("Insufficient Balance")
            else:
                pay.bal = float(pay.bal) - float(tamount)
                pay.save()

    pro = crops.objects.get(pid=request.POST.get('pid'))
    db = orders(uid=udata, pid=pro,pname=request.POST.get('pname'), quantity=request.POST.get('q1'),
                price=request.POST.get('total'),fname=request.POST.get('fname') ,lname=request.POST.get('lname') ,
                ph=request.POST.get('ph'), Add1=request.POST.get('add1'),Add2=request.POST.get('add2'),
                Add3=request.POST.get('add3'), odate=datetime.datetime.now(),card=request.POST.get('card') )

    db.save()

    return HttpResponse("entered")
   














#this for testing purpose function
def testing(request):
#     testobj=userregister.objects.all()
#     return render(request,'admin/test.html',{'testing':testobj})
    return render(request,'admin/test.html')


 

