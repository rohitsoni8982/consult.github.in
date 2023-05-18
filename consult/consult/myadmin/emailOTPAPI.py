def sendMail(email,gotp):
	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from . import views
	
	me = "rohitsoni8982@gmail.com"
	you = email

	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Verification Mail CONSULT.com"
	msg['From'] = me
	msg['To'] = you
	otp= gotp
	html = """<html>
  					<head></head>
  					<body>
    					<h1>Welcome to CONSULT.com</h1>
    					<p>You have successfully registered , please click on the link below to verify your account</p>
    					<h2>Username : """+email+"""</h2>
					    <h2>otp:-"""+str(otp)+"""
    					<br>
  					</body>
				</html>
			"""
	
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login("rohitsoni8982@gmail.com", "ywzaaimdxujbifhf") 
	
	part2 = MIMEText(html, 'html')

	msg.attach(part2)
	
	s.sendmail(me,you, str(msg)) 
	s.quit() 
	print("mail send successfully....")
	print(otp)