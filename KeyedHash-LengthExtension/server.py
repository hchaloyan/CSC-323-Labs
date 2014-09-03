import web, urllib
import crypto

mac = crypto.KeyedMAC()
render = web.template.render('templates/')
urls = ('/', 'index',
		'/post', 'post')

#This is all stuff to fake a database
posts = []
post_counter = 0
all_posts = []
f = open("static/whosonfirst.txt", "r")
for l in f:
	who,what = l.split(":")
	all_posts.append([who, what[:-1], mac.mac_post(what[:-1])])

class index:

	def GET(self):
		user_data = web.input(who="",what="",mac="", _unicode=False)
		
		if user_data.who == "" or user_data.what == "" or user_data.mac == "":
			return render.generic(posts, "Invalid post.")
		try:
			int(user_data.mac, 16)
		except:
			return render.generic(posts, "Signature must be in hex.")
		
		if mac.verify_post(user_data.what, user_data.mac):
			try:
				unicode(user_data.what)
			except:
				user_data.what = urllib.quote(user_data.what)
			posts.append([user_data.who, user_data.what, user_data.mac])
			return render.generic(posts, "")
		else:
			return render.generic(posts, "Invalid signature.")
			
class post:
	def GET(self):
		global post_counter
		who, what, mac = all_posts[post_counter]
		post_counter = (post_counter + 1)%len(all_posts)
		raise web.seeother("/?who=" + who + "&what=" + what + "&mac=" + mac)

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()