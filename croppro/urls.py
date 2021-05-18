"""croppro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from croppro import settings
from django.conf.urls.static import static
from cropapp import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('index/',views.index),
    path('about/',views.about),
    path('aboutuser/',views.aboutuser),
    path('aboutadmin/',views.aboutadmin),
    path('contactuser/',views.contactuser),
    path('contactadmin/',views.contactadmin),
    path('contact/',views.contact),
    path('adminbase/',views.adminbase),
    path('userbase/',views.userbase),
    path('signuppage/',views.signup),
    path('userdetails/',views.user_details),
    path('testing/',views.testing),
    path('userlogin/',views.login),
    path('soiltest/',views.soiltest),
    path('soilprediction/',views.soilPredictionDb),
    path('weathertest/',views.weathertest),
    path('weatherprediction/',views.weatherPredictionDb),
    path('userhome/',views.userhome),
    path('adminhome/',views.adminhome),
    path('addproduct/',views.addproduct),
    path('additemdb/',views.addItemdb),
    path('productview/',views.productview),
    path('order/',views.order),
    path('buynow/',views.buynow),
    path('manageaccount/',views.manage_account),
    path('addaccount/',views.userAddMoney),
    path('placeorder/',views.placeOrder),
    path('editproduct/',views.editproduct),
    path('updatecrop/',views.updatecropdb),
    path('orderdetail/',views.orderdetail),
    path('manageOrder/',views.manageorder),
    path('viewOldOrders/',views.viewOldOrders),
    path('orderDetails/',views.orderDetails),
    path('cancelOrder/',views.cancelOrder),
    path('deletecrop/',views.deletecrop),
    path('messagetoAdmin/',views.messagetoAdminPage),
    path('messageDb/',views.messageDb),
    path('adViewMessages/',views.adViewMessages),
    path('qReplyDb/',views.qReplyDb),
    path('logout/',views.logout),
    path('changeaddress/',views.changeaddress),
    path('updateuser/',views.updateuser),
    path('userupdate/', views.userpass),
    
    




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
