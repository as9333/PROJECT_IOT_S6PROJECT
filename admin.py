from flask import*
# from database import*
import uuid


admin=Blueprint('admin',__name__)

@admin.route('home',methods=['post','get'])
def home():

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

