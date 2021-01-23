from django.shortcuts import render

# Create your views here.

from manager.models import Manager
from subscription.models import Subscription
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password,check_password

import datetime

# go to login page -- main page
def login(req):
    return render(req,'login.html',
                  {'manager':Manager.dummy_manager(),
                   'msg': '',
                   'error': ''})

#go to registration page
def register(req):
    return render(req,'register.html',
                  {'manager':Manager.dummy_manager(),
                   'msg': '',
                   'error': ''})

#if user name invalid
def invalid_username(username):
    for x in username:
        if x.isalpha() or x.isspace():
            pass
        else:
            return True

#if invalid gmail account
def invalid_email(email):
    mail = email.split('@')
    if not mail[1]=='gmail.com':
        return True

#if manager record already exists
def duplicate_email(email):
    return Manager.objects.filter(email=email)

#if invalid date or next date
def invalid_date(date):
    #print(date)
    if datetime.datetime.strptime(date,"%Y-%m-%d").date() >= datetime.date.today():
        return True

#if in company textbox any number
def invalid_company(company):
    for x in company:
        # if x.isalpha() or x.isspace():
        if x.isdigit():
            return True
        else:
            pass

#save registration in DB
class RegisterSave(APIView):
    def get(self,req):
        return render(req, 'register.html',
                      {'manager': Manager.dummy_manager(),
                       'msg': '',
                       'error': ''})

    def post(self,req):
        formdata = req.POST

        fName = formdata['firstname']
        lName = formdata['lastname']
        email = formdata['email']
        password = formdata['password']
        address = formdata['address']
        dob = formdata['dob']
        company = formdata['company']

        #if all fields empty
        if fName=="" or lName=="" or email=="" or password=="" or address=="" or dob=="" or company=="":
            return render(req, 'register.html',
                          {'manager': {'fName':fName,'lName':lName,'email':email,
                          'address':address,'dob':dob,'company':company},
                           'msg': '',
                           'error': 'Invalid Credentials...'})

        invalidFName = invalid_username(fName) #check first name valid or not
        if invalidFName:
            return render(req, 'register.html',
                          {'manager': {'fName': fName, 'lName': lName, 'email': email,
                                       'address': address, 'dob': dob, 'company': company},
                           'msg': '',
                           'error': 'Invalid First Name...'})

        invalidLName = invalid_username(lName)  #check last name valid or not
        if invalidLName:
            return render(req, 'register.html',
                          {'manager': {'fName': fName, 'lName': lName, 'email': email,
                                       'address': address, 'dob': dob, 'company': company},
                           'msg': '',
                           'error': 'Invalid Last Name...'})

        invalidEmail = invalid_email(email) #check email valid or not
        if invalidEmail:
            return render(req, 'register.html',
                          {'manager': {'fName': fName, 'lName': lName, 'email': email,
                                       'address': address, 'dob': dob, 'company': company},
                           'msg': '',
                           'error': 'Invalid Email Id...'})

        duplicateEmail = duplicate_email(email)     #check email duplicate or not
        if duplicateEmail:
            return render(req, 'login.html',
                          {'manager': {'fName': fName, 'lName': lName, 'email': email,
                                       'address': address, 'dob': dob, 'company': company},
                           'msg': '',
                           'error': 'User Already Exists...'})

        invalidDate = invalid_date(dob)     #check DOB valid or not
        if invalidDate:
            return render(req, 'register.html',
                          {'manager': {'fName': fName, 'lName': lName, 'email': email,
                                       'address': address, 'dob': dob, 'company': company},
                           'msg': '',
                           'error': 'Invalid Date...'})

        invalidCompany = invalid_company(company)       #check company name valid or not
        if invalidCompany:
            return render(req, 'register.html',
                          {'manager': {'fName': fName, 'lName': lName, 'email': email,
                                       'address': address, 'dob': dob, 'company': company},
                           'msg': '',
                           'error': 'Invalid Company Name...'})

        hash_pass = make_password(password)  # make_password is create encrypt password
        # print('-----------pass hash:', hash_pass)
        addManager = Manager(fName=fName,lName=lName,email=email,password=hash_pass,
                          address=address,dob=dob,company=company)
        addManager.save()       #save manager registration

        return render(req, 'login.html',
                      {'manager': addManager,
                       'msg': 'User Registration Successfully...',
                       'error': ''})    #after refistration go to login page

#login credentials
class LoginSuccess(APIView):
    def get(self,req):
        return render(req, 'login.html',
                      {'manager': Manager.dummy_manager(),
                       'msg': '',
                       'error': ''})

    def post(self,req):
        formdata = req.POST
        email = formdata['email']
        password = formdata['password']

        if email=="" or password=="":  #check empty textbox
            return render(req, 'login.html',
                          {'manager':{'email':email},
                           'msg':'',
                           'error':'Invalid Credentials...'})

        invalidEmail = invalid_email(email)     #check email valid or not
        if invalidEmail:
            return render(req, 'login.html',
                          {'manager': {'email':email},
                           'msg': '',
                           'error': 'Invalid Email Id...'})

        manager = Manager.objects.filter(email=email).first()
        if manager: #if manager is available
            # check password decrypted format  #password hashing
            check_pass = check_password(password,manager.password)
            if check_pass:  #if correct password
                req.session['email'] = manager.email    #create session with mail id
                return render(req, 'home.html',
                              {'manager': {'fName': manager.fName, 'lName': manager.lName, 'email': manager.email,
                                           'address': manager.address, 'dob': manager.dob, 'company': manager.company},
                               'msg': 'Welcome...',
                               'error': ''})
            else:   #if invalid credential
                return render(req, 'login.html',
                              {'manager': {'email':email},
                               'msg': '',
                               'error': 'Invalid Password...'})
        else: #if manager is not registered
            return render(req, 'register.html',
                          {'manager': {'email':email},
                           'msg': '',
                           'error': 'Invalid User...Register First...'})

#if session is clear
def user_loginout(req):
    if req.session.has_key('email'):
        del req.session['email']
        return render(req, 'login.html',
                      {'manager': Manager.dummy_manager(),
                       'msg': 'Logout...',
                       'error': ''})
    else:
        return render(req, 'login.html',
                      {'manager': Manager.dummy_manager(),
                       'msg': '',
                       'error': 'Login First...'})

#go to home page
def home_page(req):
    if not req.session.has_key('email'):
        return user_loginout(req)

    manager = Manager.objects.filter(email = req.session['email']).first()
    return render(req, 'home.html',
                  {'manager': manager,
                   'msg': '',
                   'error': ''})

#colect all activate plance and canceled plans
def all_plans(req):
    active_subscription = []  # all active subscription and not expired
    canceled_subscription = []  # all inactive subscription and not expired
    manager = Manager.objects.filter(email=req.session['email']).first()

    # collect all subscriptions ot that manager
    all_subcriptions = Subscription.objects.filter(mangerref=manager.id).all()
    for subcription in all_subcriptions:    #iterate subscriptions
        # print(subcription.id)
        expire_date = subcription.expireDate
        today_date = datetime.date.today()
        if today_date > expire_date:  # check subscription expire or not if expire do inactivate
            if subcription.active == 'Yes':  # check its activate or not
                subcription.active = 'No'
                subcription.expire = 'Yes'
                subcription.save()
        elif subcription.active == 'No' and subcription.expire == 'No':  # if not expire but inactive
            canceled_subscription.append(subcription)    # append inactivate subscription and not expired
        elif subcription.active == 'Yes' and subcription.expire == 'No':  # activate record and not expired
            active_subscription.append(subcription)     # append activate subscription and not expired

    # print(active_subscription)
    # print(canceled_subscription)
    return active_subscription,canceled_subscription,manager

#go to your subscriptions
def your_plans(req):
    if not req.session.has_key('email'):
        return user_loginout(req)

    sub=all_plans(req)      #call all_plance function
    active_subscription = sub[0]
    canceled_subscription = sub[1]
    manager = sub[2]
    return render(req, 'your_plans.html',
                  {'manager': manager,
                   'active_subscription':active_subscription,
                   'canceled_subscription':canceled_subscription,
                   'msg': '',
                   'error': ''})

#go to cancel subscription
def your_plans_cancel(req,sid):
    if not req.session.has_key('email'):
        return user_loginout(req)

    manager = Manager.objects.filter(email=req.session['email']).first()

    subcription_detail = Subscription.objects.filter(id=sid,mangerref=manager.id).first()
    if subcription_detail:      #if record
        #check activate and not expired
        if subcription_detail.active=='Yes' and subcription_detail.expire=='No':
            subcription_detail.active='No'
            subcription_detail.save()

        sub = all_plans(req)
        active_subscription = sub[0]
        canceled_subscription = sub[1]
        # manager = sub[2]
        return render(req, 'your_plans.html',
                      {'manager': manager,
                       'active_subscription':active_subscription,
                       'canceled_subscription':canceled_subscription,
                       'msg': 'Your Subscription is Canceled...',
                       'error': ''})
    else: #if invalid subscription id or invalid manager
        sub = all_plans(req)
        active_subscription = sub[0]
        canceled_subscription = sub[1]
        # manager = sub[2]
        return render(req, 'your_plans.html',
                      {'manager': manager,
                       'active_subscription': active_subscription,
                       'canceled_subscription': canceled_subscription,
                       'msg': 'Invalid Credentials...',
                       'error': ''})

#go to resume subscriptions
def your_plans_resume(req,sid):
    if not req.session.has_key('email'):
        return user_loginout(req)

    manager = Manager.objects.filter(email=req.session['email']).first()

    subcription_detail = Subscription.objects.filter(id=sid,mangerref=manager.id).first()
    if subcription_detail:  #if record
        #check not expire but inactivate
        if subcription_detail.active=='No' and subcription_detail.expire=='No':
            subcription_detail.active='Yes'     #then activate that record
            subcription_detail.save()

        sub = all_plans(req)
        active_subscription = sub[0]
        canceled_subscription = sub[1]
        # manager = sub[2]
        return render(req, 'your_plans.html',
                      {'manager': manager,
                       'active_subscription':active_subscription,
                       'canceled_subscription':canceled_subscription,
                       'msg': 'Your Subscription is Resumed...',
                       'error': ''})
    else:   #if invalid subscriptions id or invalid manager
        sub = all_plans(req)
        active_subscription = sub[0]
        canceled_subscription = sub[1]
        # manager = sub[2]
        return render(req, 'your_plans.html',
                      {'manager': manager,
                       'active_subscription': active_subscription,
                       'canceled_subscription': canceled_subscription,
                       'msg': 'Invalid Credentials...',
                       'error': ''})
