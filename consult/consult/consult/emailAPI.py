def sendMail(email,password):
	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	
	me = "rohitsoni8982@gmail.com"
	you = email

	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Verification Mail CONSULT.com"
	msg['From'] = me
	msg['To'] = you

	html = """<html>
  					<head></head>
  					<body>
    					<h1>Welcome to CONSULT.com</h1>
    					<p>You have successfully registered , please click on the link below to verify your account</p>
    					<h2>Username : """+email+"""</h2>
    					<h2>Password : """+str(password)+"""</h2>
    					<br>
    					<a href='http://localhost:8000/verify?vemail="""+email+"""' >Click here to verify account</a>		
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