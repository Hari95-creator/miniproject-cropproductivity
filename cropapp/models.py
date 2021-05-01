from django.db import models

# Create your models here.
class userregister(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    uname=models.CharField(max_length=100,unique=True)
    pwd=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=13,unique=True)

class admin(models.Model):
    uname=models.CharField(max_length=100)
    pwd=models.CharField(max_length=100)
    email=models.EmailField(unique=True)

class crops(models.Model):
    pid=models.AutoField(primary_key=True,unique=True)
    pname= models.CharField(max_length=100)
    price=models.IntegerField()
    desc=models.TextField()
    img=models.ImageField(upload_to="itemPic/")

class orders(models.Model):
    oid=models.AutoField(primary_key=True,unique=True)
    uid=models.ForeignKey(userregister,on_delete=models.CASCADE)
    pid = models.ForeignKey(crops,on_delete=models.CASCADE)
    pname = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.IntegerField()
    card= models.CharField(max_length=15)
    fname= models.CharField(max_length=250)
    lname= models.CharField(max_length=250)
    ph = models.CharField(max_length=250)
    Add1 = models.CharField(max_length=250)
    Add2 = models.CharField(max_length=250)
    Add3 = models.CharField(max_length=250)
    odate = models.DateField()  # order date
    ddate = models.DateField(max_length=30, blank=True, null=True)  # store expected delivery date&delivered date
    status = models.CharField(max_length=100, default='pending')


class account(models.Model):
    cardnum=models.CharField(max_length=60,unique=True)
    cvv=models.CharField(max_length=10)
    bal=models.IntegerField()

class soilPrediction(models.Model):
    pno=models.AutoField(primary_key=True)
    uid=models.ForeignKey(userregister,on_delete=models.CASCADE)
    cal=models.FloatField()
    mag=models.FloatField()
    po=models.FloatField()
    sul=models.FloatField()
    nit=models.FloatField()
    lim=models.FloatField()
    carb=models.FloatField()
    phos=models.FloatField()
    moist=models.FloatField()
    result=models.CharField(max_length=40)

class weatherPrediction(models.Model):
    pno=models.AutoField(primary_key=True)
    uid=models.ForeignKey(userregister,on_delete=models.CASCADE)
    temp=models.FloatField()
    hum=models.FloatField()
    ph=models.FloatField()
    rain=models.FloatField()
    result=models.CharField(max_length=40)


