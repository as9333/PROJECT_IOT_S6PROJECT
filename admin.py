from flask import*
from database import*
import uuid


admin=Blueprint('admin',__name__)

@admin.route('home',methods=['post','get'])
def home():

	if not session.get('logged_in'):
		return redirect(url_for("public.login"))
	else:	
		return render_template('adminhome.html')

@admin.route('view',methods=['post','get'])
def view():
	data={}
	q="select * from registeration"
	result=select(q)
	data['viewreg']=result
	return render_template('view.html',data=data)

@admin.route('/registerproduct',methods=['get','post'])
def registerproduct():
	data={}
	if 'submit' in request.form:
		productname=request.form['productname']
		price=request.form['price']
		# img=request.file['productpic']
		# path='static/uploads/'+str(uuid.uuid4())+img.filename
		# img.save(path)


		q="insert into producttable values(null,'%s',null,'%s')"%(productname,price)
		insert(q)

	return render_template('product.html',data=data)

@admin.route('/add_user',methods=['get','post'])
def add_user():

	if not session.get('logged_in'):
		return redirect(url_for("public.login"))
	else:	
		
		if 'submit' in request.form:
			username=request.form['username']
			password=request.form['pass']
			q="INSERT INTO `login` VALUES (NULL,'%s','%s','user')"%(username,password)
			id=insert(q)
			return "<script>window.alert('USER ADDED SUCCESSFULLY');window.location.replace('/admin/add_user');</script>"

		return render_template("reg.html")	

@admin.route('/delete_user',methods=['get','post'])
def delete_user():

	mydatabase = mysql.connector.connect(
    	host = 'localhost', user = 'root',
    	passwd = '', database = 'smart_switch')

	mycursor = mydatabase.cursor()

	if 'submit' in request.form:
		user_id=request.form['user_id']
		print("USER_id to delete=",user_id)	
		

		q="DELETE FROM `login` WHERE `login`.`login_id` = %s"%(user_id)
		delete(q)
		# return "<script>window.alert('USER DELETEED SUCCESSFULLY');window.location.replace('/admin/delete_user');</script>"

	if not session.get('logged_in'):
		return redirect(url_for("public.login"))
	else:	

		mycursor.execute('SELECT * FROM login')
		data=mycursor.fetchall()
		mydatabase.close()	
		return render_template('delete_user.html',output_data=data)
		
		

		# return render_template("reg.html")	



	

