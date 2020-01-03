from flask import *
from database import *
from public import public
from admin import admin
import requests
import os
import mysql.connector
import schedule
import time
import threading
import pyduktape #pip install pyduktape, also download
app = Flask(__name__)

mydatabase = mysql.connector.connect(
    host = 'localhost', user = 'root',
    passwd = '', database = 'smart_switch')

mycursor = mydatabase.cursor()
final=[]

def check_db_for_jobs():
    
    global run_once
    # print("Current run_once value on running before if condition=", run_once)
    global jobs_original
    global jobs_original_row
    global jobs_row

    if run_once == 0:                                                                       #This if condition is used to assign initial value to jobs_original variable otherwise error apperas
        mycursor.execute('SELECT from_time, to_time, status, relay FROM automatic_jobs')
        jobs_original = mycursor.fetchall()
        run_once = 1

    # print("Current run_once value running after if condition=", run_once)
    mycursor.execute('SELECT from_time, to_time, status, relay FROM automatic_jobs')
    # print("Entered check_db_for_jobs function")
    # print(mycursor.fetchall())          #DO NOT CALL FETCHALL TWICE NOT WORK
    jobs = mycursor.fetchall()
    
    if jobs != jobs_original:


        print("Entered if condition on checking jobs with jobs and VALUE CHANGED!!!!!")  #here we can enter code to execute if the database has changed 
        print("OLD jobs=",jobs_original)
        print("OLD JOBS length=",len(jobs_original))                                        #the len() returns the rows in jobs_original and jobs
        print("new jobs=",jobs)
        print("new JOBS length=",len(jobs))
        # print("OLD jobs 1st row=",jobs_original[0][3])    #this method returns 1st row 1st coloum value that is from_time value of 1st row


        jobs_original_row=len(jobs_original)
        jobs_row=len(jobs)

        if jobs_original_row < jobs_row:                #this means that a new row has been created that is a new job has been entered by the user
            print("A NEW JOB HAS BEEN ENTERED!!!")
            print("Newly entered job is=",jobs[jobs_row-1])   #this logic enables us to find the newly entered job "jobs[jobs_row-1]" where jobs_row variable contains the table automatic_jobs's rows since array starts from 0 jobs_rows-1 give the newly entered job 

            if jobs[jobs_row-1][2] == 'ON':                  # jobs[jobs_row-1][2] gives to on or off the relay from 'from time' to 'to_time'

                print("Entered ON condition")
                from_time=jobs[jobs_row-1][0]                # jobs[jobs_row-1][0] gives from_time
                print("FROM TIME=",from_time)
                to_time=jobs[jobs_row-1][1]                  # jobs[jobs_row-1][1] gives to_time
                print("TO TIME=",to_time)
                relay=jobs[jobs_row-1][3]                    # jobs[jobs_row-1][3] gives which relay to on/off
                print("Relay=",relay)

                schedule.every().day.at(from_time).do(pin_on, relay)
                print("(CALLED FROM ON CONDITION)SHEDULED JOB to pin_on function from_time=",from_time)

                schedule.every().day.at(to_time).do(pin_off, relay)
                print("(CALLED FROM ON CONDITION)SHEDULED JOB to pin_off function to_time=",to_time)

                # while True:
                #     schedule.run_pending()
                #     time.sleep(1)

            if jobs[jobs_row-1][2] == 'OFF':

                print("Entered OFF condition")
                from_time=jobs[jobs_row-1][0]
                print("FROM TIME=",from_time)
                to_time=jobs[jobs_row-1][1]
                print("TO TIME=",to_time)
                relay=jobs[jobs_row-1][3]
                print("Relay=",relay)    

                schedule.every().day.at(from_time).do(pin_off, relay)
                print("(CALLED FROM OFF CONDITION)SHEDULED JOB to pin_off function from_time=",from_time)

                schedule.every().day.at(to_time).do(pin_on, relay)
                print("(CALLED FROM OFF CONDITION)SHEDULED JOB to pin_on function to_time=",to_time)

                # while True:
                #     schedule.run_pending()
                #     time.sleep(1) 

        
        if jobs_original_row > jobs_row:                #this means that a  row has been deleted that is a  job has been removed by the user
            print("A  JOB HAS BEEN DELETED!!!")


        jobs_original=jobs                                                               # database table changes such as add or removing a row

    # for x in jobs:
    #     print(x[0])                         #THIS LINE prints differet coloums by changing value 0 to 1 and so on
    #     final.append(x[0])


    # print("jobs[0][0]=",jobs[0][0])
    # print("jobs[0][1]=",jobs[0][1])
    # print("jobs[0][2]=",jobs[0][2])
    # print("jobs[0][3]=",jobs[0][3])
    # print("jobs[0][4]=",jobs[0][4])
    # print(jobs_from_db)
    # print(mycursor)
    # print("VALUE FROM VARIABLE JOBS")
    # print(jobs)


# def test():
#     print("This is from test fn called by shedule 1")


app.register_blueprint(public,url_prefix='/')
app.register_blueprint(admin,url_prefix='/admin')
app.secret_key = os.urandom(12)


def shedule_function():
    global run_once
    global jobs_original_row
    global jobs_row
    global auth_code
    auth_code="4LrnMs0PkPlgyC6GDKrzBJYLdDZDjmfi"
    run_once = 0
    print("Entered the shedule_fn")                                #this function is used to execute the functon check_db_for_jobs as a thread
    schedule.every(3).seconds.do(check_db_for_jobs)

    # schedule.every().day.at("01:13").do(test)
    # schedule.every().day.at("01:13").do(test)

    while True:
        schedule.run_pending()
        time.sleep(1)


# def pin_on(relay):
#     print("Entered pin_on function with relay=",relay)
#     global auth_code
#     context = pyduktape.DuktapeContext()
#     context.set_globals(pin=relay, auth_code=auth_code)   #Here the blue coloured variables (pin and authcode(on LEFTSIDE)) is the javascript global variables
#     context.eval_js_file('pin_on.js')

# def pin_off(relay):
#     print("Entered pin_off function with relay=",relay)
#     global auth_code
#     context = pyduktape.DuktapeContext()
#     context.set_globals(pin=relay, auth_code=auth_code)
#     context.eval_js_file('pin_off.js')

def pin_on(relay):
    print("Entered pin_on function with relay=",relay)
    global auth_code
    # url = "http://blynk-cloud.com/"auth_code"/update/"relay"?value=0"
    url="http://blynk-cloud.com/%s/update/%s?value=0"%(auth_code,relay)
    print("URL=",url)
    response = requests.get(url)

def pin_off(relay):
    print("Entered pin_off function with relay=",relay)
    global auth_code
    url="http://blynk-cloud.com/%s/update/%s?value=1"%(auth_code,relay)
    print("URL=",url)
    response = requests.get(url)


t = threading.Thread(target=shedule_function)
t.daemon = True
t.start()
app.run(debug=False,port='5001')
