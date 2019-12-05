from flask import *
from database  import *

app = Flask(__name__)

@app.route('/',methods=['get','post'])
def login():

	# if 'submit' in request.form:
	# 	user=request.form['username']
	# 	pas=request.form['password']

	# 	q="select * from login where username='%s' and password='%s'"%(user,pas)
	# 	res=select(q)

	# 	if res:
	# 		if res[0]['usertype']=="admin":
	# 			return redirect(url_for("admin.home"))
	# 		elif res[0]['usertype']=="user":
	# 			return redirect(url_for("public.home"))

	return render_template("login.html")

if __name__=="__main__":
    app.run()