from django.http import HttpResponse
from django.shortcuts import render,redirect
from . import emailAPI
from . import models
import time

#middleware to check session for mainapp routes
def sessioncheck_middleware(get_response):
	def middleware(request):
		if request.path=='/home/' or request.path=='/about/' or request.path=='/contact/' or request.path=='/login/' or request.path=='/service/' or request.path=='/register/':
			request.session['sunm']=None
			request.session['srole']=None
			response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

def home(request):
    # to check a session 
    # print(request.session["srole"])
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def service(request):
    return render(request,"service.html")

def blog(request):
    return render(request,"blog.html")

def detail(request):
    return render(request,"detail.html")

def contact(request):
    return render(request,"contact.html")

def register(request):
    if request.method=="GET":
        return render(request,"register.html",{"output":""})
    else:
        #fatechin the data are given the html(field) 
        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        mobile=request.POST.get("mobile")
        city=request.POST.get("city")
        address=request.POST.get("address")
        gender=request.POST.get("gender")
        info=time.asctime()
        # to send email to verify
        emailAPI.sendMail(email,password)
        # to save userdetails in a databases
        db=models.Register(name=name,email=email,password=password,mobile=mobile,city=city,address=address,gender=gender,info=info,role="user",status=0)
        db.save()

    return render(request,"register.html",{"output":"register form success fully..."})

def verify(request):
    vemail=request.GET.get("vemail")
    models.Register.objects.filter(email=vemail).update(status=1)
    return redirect("/login/")

def checkEmailAvaibility(request):
    emailid=request.GET.get("emailid")
    userDetails=models.Register.objects.filter(email__startswith=emailid)
    if len(userDetails)>0:
        return HttpResponse(1)
    else:      
        return HttpResponse(0)

def login(request):
    cunm,cpass="",""
    if request.COOKIES.get("cunm")!=None:
        cunm=request.COOKIES.get("cunm")
        cpass=request.COOKIES.get("cpass")

    if request.method=="GET":
        return render(request,"login.html",{"output":"","cunm":cunm,"cpass":cpass})
    else:
        #to get user details to make login
        email=request.POST.get("email")
        password=request.POST.get("password")
        # print(email,password) -->print in cmd
        #to check a details in a databases
        userDetails=models.Register.objects.filter(email=email,password=password,status=1)
         #to check valid user login
        if len(userDetails)>0:
            # to set a session 
            request.session["sunm"]=userDetails[0].email
            request.session["srole"]=userDetails[0].role
            # to redirect a admin and user panel
            if userDetails[0].role=="admin":
                response = redirect("/myadmin/")
            else:
                response = redirect("/user/")
                
            # to set a userdetails in cookies
            chk=request.POST.get("chk")
            if chk!=None:
                response.set_cookie("cunm",userDetails[0].email,max_age=3600*24*365)
                response.set_cookie("cpass",userDetails[0].password,max_age=3600*24*365)
            return response
        else:
            return render(request,"login.html",{"output":"invalid id plase login again..","cunm":cunm,"cpass":cpass})
