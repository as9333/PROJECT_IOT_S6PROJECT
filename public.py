from flask import *
from database  import *
import uuid

public=Blueprint('public',__name__)

@public.route('/home',methods=['post','get'])
def home():

	return render_template('publichome.html')


@public.route('viewproduct',methods=['post','get'])
def view():
	data={}
	q="select * from producttable"
	result=select(q)
	data['viewreg']=result
	return render_template('viewproduct.html',data=data)


@public.route('/',methods=['get','post'])
def login():

	if 'submit' in request.form:
		user=request.form['username']
		pas=request.form['password']

		q="select * from login where username='%s' and password='%s'"%(user,pas)
		res=select(q)

		if res:
			if res[0]['usertype']=="admin":
				return redirect(url_for("admin.home"))
			elif res[0]['usertype']=="user":
				return redirect(url_for("public.home"))

	return render_template("login.html")


@public.route('/registration',methods=['get','post'])
def registration():
	data={}
	if 'submit' in request.form:
		name=request.form['name']
		password=request.form['pass']
		address=request.form['address']
		phno=request.form['phone_number']
		gender=request.form['gender']
		username=request.form['username']
		img=request.files['profile_pic']
		path='static/uploads/'+str(uuid.uuid4())+img.filename
		img.save(path)

		q="INSERT INTO `login` VALUES (NULL,'%s','%s','user')"%(username,password)
		id=insert(q)


		q="INSERT INTO registeration VALUES (null,'%s','%s','%s','%s','%s','/%s')"%(id,name,address,phno,gender,path)
		res=insert(q)

		return redirect(url_for("public.login"))

	q="select * from registeration"
	result=select(q)
	data['viewreg']=result
	return render_template("reg.html",data=data)

