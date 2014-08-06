import web
from web import form
import MT19937
import base64, datetime, hashlib

TIMEOUT = 5		# token timeout, in minutes

render = web.template.render('templates/')
urls = ('/', 'index',
        '/forgot', 'forgot',
        '/register', 'register',
        '/reset', 'reset')

user_dic = {"admin":"119ba0f0a97158cd4c92f9ee6cf2f29e75f5e05a"}
token_dic = {}

#Seed my super-secure PRNG with a roll of a die, which we all know is truly random
MT = MT19937.MT19937(4)

class index:
	myform = form.Form(
		form.Textbox("username",
			form.notnull,
			description="Username",
			id='usernameBox'),
		form.Password("password",
			form.notnull,
			description="Password",
			id='passwordBox'),
		form.Button("Login",
			id='loginButton'))

	def GET(self):
		form = self.myform()
		return render.login(form, "")
   
	def POST(self):
		form = self.myform()

		if not form.validates():
			return render.login(form,"")

		user = form.d.username
		pw = hashlib.sha1(form.d.password).hexdigest()

		if user == "admin" and user_dic["admin"] == pw:
			return render.loggedin(user, True)
		elif user in user_dic and user_dic[user] == pw:
			return render.loggedin(user, False)
		else:
			return render.login(form,"Username/Password Incorrect")

class forgot:
	myform = form.Form(
		form.Textbox("email",
			form.notnull,
			description = "Username",
			id='forgotEmail'),
		form.Button("Reset",
			description="Send"),
			id='forgotButton')

	nullform = form.Form()

	def GET(self):
		form = self.myform()
		return render.generic(form, "Enter your username to reset your password. A password reset token will be mailed to you.","")

	def POST(self):
		form = self.myform()
		msg = "Enter your username to reset your password. A password reset token will be mailed to you."
		err = ""

		if not form.validates():
			err = "Invalid form data"
			return render.generic(form, msg, err)

		email = form.d.email
         
		if email in user_dic:
			token = generate_token()
			time = datetime.datetime.now() + datetime.timedelta(minutes=TIMEOUT)
			token_dic[token] = reset_token(email, time)

			if email == "admin":
				msg = "Admin emailed reset token."
			else:
				#TODO: Email server not work, so I'll just post them to the screen for now.
				msg = web.ctx.env.get('HTTP_HOST') + "/reset?token=" + token
				return render.generic(form, msg, err)
		else:
			err = "User not found."

		return render.generic(form, msg, err)

class register:
	myform = form.Form(
		form.Textbox("email",
			form.notnull,
			description = "Username"),
		form.Password("password",
			form.notnull,
			description = "Password"),
		form.Button("Register",
			description="Register"))
			
	nullform = form.Form()
   
	def GET(self):
		form = self.myform()
		return render.generic(form, "Enter a username and password.", "")

	def POST(self):
		form = self.myform()
		msg = ""
		err = ""

		if not form.validates():
			err = "Invalid fields."
		else:
			if form.d.email in user_dic:
				err = "User already registered."
			else:
				user_dic[form.d.email] = hashlib.sha1(form.d.password).hexdigest();
				msg = "User registered."
		return render.generic(self.nullform(), msg, err)

class reset:
	myform = form.Form(
		form.Password("password",
			form.notnull,
			description = "New Password"),
		form.Hidden("token", 
			form.notnull,
			value="", 
			description="Reset Token"),
		form.Button("Reset Password",
			description="Register"))

	nullform = form.Form()

	def GET(self):
		user_data = web.input(token="")
		token = user_data.token

		myform = form.Form(
			form.Password("password",
				form.notnull,
				description = "New Password"),
			form.Hidden("token", 
				form.notnull, 
				value=token, 
				description="Reset Token"),
			form.Button("Reset Password",
			description="Register"))
		msg = ""
		err = ""

		if token not in token_dic:
			err = "Invalid token."
			return render.generic(self.nullform(), msg, err)

		if token_dic[token].timeout <= datetime.datetime.now():
			err = "Token expired."
			return render.generic(self.nullform(), msg, err)

		msg = "Reset Password for: " + token_dic[token].email
		return render.generic(myform, msg, err)

	def POST(self):
		form = self.myform()
		msg = ""
		err = ""

		if not form.validates():
			err = "Invalid form data."
			return render.generic(self.nullform, msg, err)

		if form.d.token in token_dic and token_dic[form.d.token].timeout > datetime.datetime.now():
			msg = "Password reset for user: " + token_dic[form.d.token].email
			email = token_dic[form.d.token].email
			user_dic[email] = hashlib.sha1(form.d.password).hexdigest();
		else:
			err = "Invalid token."

		return render.generic(self.nullform, msg, err)
   
class reset_token:
	def __init__(self, email, timeout):
		self.email = email
		self.timeout = timeout

def generate_token():
	token = bytes()
	
	#Generate a 256-bit random number as our reset tokwn so it can't be guessed
	for i in range(8):
		token += bytes(MT.extract_number())
	return base64.b64encode(token)


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()   
