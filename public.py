from flask import *
from database  import *
import uuid
import requests
import schedule  #pip install schedule
import time

public=Blueprint('public',__name__)

# @public.route('/jsfunctions',methods=['post','get'])
def pin_on():
	print("Entered fn pin_on")
	# return render_template('jsfunctions.html')
	return "Entered fn pin_on"


@public.route('/login',methods=['post','get'])
def home():

	return redirect(url_for("public.login"))

@public.route('/logout',methods=['post','get'])
def logout():

	session['logged_in'] = False
	return redirect(url_for("public.login"))


@public.route('/controlpanel',methods=['post','get'])
def controlpanel():

	if not session.get('logged_in'):
		return redirect(url_for("public.login"))
	else:	
		return render_template('ctrlpanel.html')
#     if request.method == 'POST':
#         if request.form.get('btn') == 'on':
#             return requests.get('http://blynk-cloud.com/8l5Nb4p_bbiGynNwHUV9TmjHX7ZHVZac/update/D1?value=0').content
#         # elif request.form['submit_button'] == 'Do Something Else':
#         #     pass # do something else
#         else:
#             pass # unknown
#     elif request.method == 'GET':
    

@public.route('/',methods=['get','post'])
def login():

	if 'submit' in request.form:
		user=request.form['username']
		pas=request.form['password']

		q="select * from login where username='%s' and password='%s'"%(user,pas)
		res=select(q)

		if res:
			if res[0]['usertype']=="admin":
				session['logged_in'] = True
				return redirect(url_for("admin.home"))
				
			elif res[0]['usertype']=="user":
				 session['logged_in'] = True
				 return redirect(url_for("public.controlpanel"))
				# return render_template('ctrlpanel.html')
		else:
			# return redirect(url_for("public.login"))
			return "<script>window.alert('WRONG CREDENTIALS');window.location.replace('/');</script>"
			

	return render_template("login.html")
	# return render_template("Login_v14/index.html")


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

@public.route('/automatic_on_off',methods=['post','get'])
def automatic_on_off():

	# if not session.get('logged_in'):
	# 	return redirect(url_for("public.login"))
	# else:	
		# return render_template('automatic_on_off.html')

	if 'submit' in request.form:
		from_time=request.form['from_time']	
		to_time=request.form['to_time']
		button=request.form['button']
		status=request.form['status']
		# print("from_time", file=sys.stderr)
		# print('enter getJSONReuslt', flush=True)
		print("From_time=",from_time)
		print("to_time=",to_time)
		print("button=",button)
		print("status=",status)
		pin_on()

	if not session.get('logged_in'):
		return redirect(url_for("public.login"))
	else:	
		return render_template('automatic_on_off.html')
