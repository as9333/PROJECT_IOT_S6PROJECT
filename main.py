from flask import *
from database import *
from public import public
from admin import admin
import os
app = Flask(__name__)

app.register_blueprint(public,url_prefix='/')
app.register_blueprint(admin,url_prefix='/admin')
app.secret_key = os.urandom(12)
app.run(debug='true',port='5001')