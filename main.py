from flask import *
from database import *
from public import public
from admin import admin
import os
import mysql.connector
import schedule
import time
import threading
app = Flask(__name__)

mydatabase = mysql.connector.connect(
    host = 'localhost', user = 'root',
    passwd = '', database = 'smart_switch')

mycursor = mydatabase.cursor()
final=[]

def check_db_for_jobs():
    
    global run_once
    print("Current run_once value on running before if condition=", run_once)
    global jobs_original

    if run_once == 0:                                                                       #This if condition is used to assign initial value to jobs_original variable otherwise error apperas
        mycursor.execute('SELECT from_time, to_time, status, relay FROM automatic_jobs')
        jobs_original = mycursor.fetchall()
        run_once = 1

    print("Current run_once value running after if condition=", run_once)
    mycursor.execute('SELECT from_time, to_time, status, relay FROM automatic_jobs')
    # print("Entered check_db_for_jobs function")
    # print(mycursor.fetchall())          #DO NOT CALL FETCHALL TWICE NOT WORK
    jobs = mycursor.fetchall()
    
    if jobs != jobs_original:
        print("Entered if condition on checking jobs with jobs and VALUE CHANGED!!!!!")  #here we can enter code to execute if the database has changed 
        jobs_original=jobs                                                               # database table changes such as add or removing a row

    for x in jobs:
        print(x[0])                         #THIS LINE prints differet coloums by changing value 0 to 1 and so on
        final.append(x[0])
    # print(jobs_from_db)
    # print(mycursor)
    # print("VALUE FROM VARIABLE JOBS")
    # print(jobs)


def test():
    print("This is from test fn called by shedule 1")


app.register_blueprint(public,url_prefix='/')
app.register_blueprint(admin,url_prefix='/admin')
app.secret_key = os.urandom(12)


def shedule_function():
    global run_once
    run_once = 0
    print("Entered the shedule_fn")                                #this function is used to execute the functon check_db_for_jobs as a thread
    schedule.every(3).seconds.do(check_db_for_jobs)

    # schedule.every().day.at("01:13").do(test)
    # schedule.every().day.at("01:13").do(test)

    while True:
        schedule.run_pending()
        time.sleep(1)


t = threading.Thread(target=shedule_function)
t.daemon = True
t.start()
app.run(debug=False,port='5001')
