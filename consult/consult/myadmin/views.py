from django.shortcuts import render,redirect
from django.http import HttpResponse
from consult import models as consult_models
from . import emailOTPAPI 
import random

#middleware to check session for admin routes
def sessioncheckmyadmin_middleware(get_response):
	def middleware(request):
		if request.path=='/myadmin/' or request.path=='/myadmin/profile/' or request.path=='/myadmin/changepassword/':
			if request.session['sunm']==None or request.session['srole']!="admin":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

def adminhome(request):
	#to check otp in a session
	# otp=request.session["otp"]
	# print("admin home otp:-",otp)
	return render(request,"admin_home.html",{"sunm":request.session['sunm'],"srole":request.session['srole']})

def manageuser(request):
	clist=consult_models.Register.objects.filter(role="user")
	return render(request,"manageuser.html",{"clist":clist})

def manageuserstatus(request):
	regid=int(request.GET.get("regid"))
	s=request.GET.get("s")
	if s=="block":
		consult_models.Register.objects.filter(regid=regid).update(status=0)
	elif s=="verify":
		consult_models.Register.objects.filter(regid=regid).update(status=1)
	else:
		consult_models.Register.objects.filter(regid=regid).delete()
	return redirect("/myadmin/manageuser")

def profile(request):
	sunm=request.session["sunm"]
	userDetails=consult_models.Register.objects.filter(email=sunm)
	m,f="",""
	if userDetails[0].gender=="male":
		m="checked"
	else:
		f="checked"
	if request.method=="GET":
		return render(request,"profile.html",{"sunm":sunm,"srole":request.session['srole'],"userDetails":userDetails[0],"m":m,"f":f})
	else:
		name=request.POST.get("name")
		email=request.POST.get("email")	  
		mobile=request.POST.get("mobile")
		address=request.POST.get("address")
		gender=request.POST.get("gender")
		consult_models.Register.objects.filter(email=email).update(name=name,email=email,mobile=mobile,address=address,gender=gender)
	return redirect("/myadmin/profile/")

def changepassword(request):
	sunm=request.session['sunm']
	if request.method=="GET":
		return render(request,"changepassword.html",{"output":"","sunm":sunm,"srole":request.session['srole']})
	else:
		opassword=request.POST.get("opassword")
		npassword=request.POST.get("npassword")
		cpassword=request.POST.get("cpassword")
		userDetails=consult_models.Register.objects.filter(email=sunm,password=opassword)
		if len(userDetails)>0:
			if npassword==cpassword:
				userDetails.update(password=cpassword)
				return redirect("/login/")
			else:
				msg="new password and comform password not match"
		else:
			msg="invalid old password"
	return render(request,"changepassword.html",{"output":msg,"sunm":sunm,"srole":request.session['srole']})		


def otp (request):
	sunm=request.session['sunm']
	srole=request.session['srole']
	otp=request.session['otp']
	if request.method=="GET":
		return render(request,"otp.html",{"output":"","sunm":sunm,"srole":srole,"otp":otp})
	else:
		cotp=request.POST.get("cotp")
		if otp==int(cotp):
			return redirect("/myadmin/changepassword")
		else:
			return render(request,"otp.html",{"output":"invalid","sunm":sunm,"srole":srole,"otp":otp})
			
		
def gernateOTP(request):
	sunm=request.session['sunm']
	otp = random.randint(1000,9999)
	# print("views otp :-",otp)
	# to send otp in a mail 
	emailOTPAPI.sendMail(sunm,otp)
	# to store otp in a session
	request.session['otp']=otp
	# print("session otp:-",request.session["otp"])
	return render(request,"otp.html",{"sunm":sunm,"srole":request.session['srole']})
