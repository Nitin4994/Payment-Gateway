from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from manager.views import user_loginout
from manager.models import Manager
from subscription.models import Subscription


from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
import datetime
from datetime import timedelta
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
#from django.core.context_processors import csrf
from django.template.context_processors import csrf



#go to payment gateway -- main task
class paymentgateway(APIView):
    def get(self,req):
        if not req.session.has_key('email'):
            return user_loginout(req)

        manager = Manager.objects.filter(email=req.session['email']).first()
        return render(req, 'home.html',
                      {'manager': manager,
                       'msg': '',
                       'error': ''})

    #if post
    def post(self,req):
        if not req.session.has_key('email'):
            return user_loginout(req)

        formdata = req.POST
        planname = formdata['planname']
        price = formdata['price']

        manager = Manager.objects.filter(email=req.session['email']).first()

        #get all subscriptions
        prievious_subscribe = Subscription.objects.filter(plan=planname,mangerref=manager.id).all()
        for i in prievious_subscribe:   #iterate subscriptions
            expire_date = i.expireDate
            today_date = datetime.date.today()
            if today_date < expire_date:    #check that plan is activate or expire
                # if activate then dont subscribe again
                return render(req, 'home.html',
                              {'manager': manager,
                               'msg': '',
                               'error': 'Your Plan already is Active...'})
        #print(manager.fName)
        posted = {'amount': price, 'firstname': manager.fName, 'email': manager.email,'phone': '',
                  'productinfo': planname, 'surl': 'http://localhost:8000/subscription/Success/', 'furl': 'http://localhost:8000/subscription/Failure/'}

        #print(posted.get('amount'))

        # ===================THIS CODE IS GETING FROM PAYUMONEY SITE===============================
        MERCHANT_KEY = "crTljknJ"       #provided by payumoney
        key = "crTljknJ"                #provided by payumoney
        SALT = "wzVKYERrfx"             #provided by payumoney
        PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
        # PAYU_BASE_URL = "https://test.payu.in/_payment"
        action = ''
        #posted = {}
        # Merchant Key and Salt provided y the PayU.
        for i in req.POST:
            print(req.POST[i])
            posted[i] = req.POST[i]
        hash_object = hashlib.sha256(b'randint(0,20)')
        txnid = hash_object.hexdigest()[0:20]
        hashh = ''
        posted['txnid'] = txnid
        hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        posted['key'] = key
        hash_string = ''
        hashVarsSeq = hashSequence.split('|')
        for i in hashVarsSeq:
            try:
                hash_string += str(posted[i])
            except Exception:
                hash_string += ''
            hash_string += '|'
        hash_string += SALT
        hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        action = PAYU_BASE_URL

        if (posted.get("key") != None and posted.get("txnid") != None and posted.get(
                "productinfo") != None and posted.get(
                "firstname") != None and posted.get("email") != None):
            #if any field empty then not pay-- get error in payumoney site
            # print(posted.get("key"))
            # print(posted.get("txnid"))
            # print(posted.get("productinfo"))
            # print(posted.get("firstname"))
            # print(posted.get("email"))
            # print(posted.get("phone"))
            # print(posted.get("surl"))
            # print(posted.get("furl"))

            return render(req, 'payumoney.html',
                          {"posted": posted, "hashh": hashh,
                           "manager": manager,
                           "MERCHANT_KEY": MERCHANT_KEY,
                           "txnid": txnid,
                           "hash_string": hash_string,
                           "action": PAYU_BASE_URL})


        else:
            return render(req, 'payumoney.html',
                          {"posted": posted, "hashh": hashh,
                           "manager": manager,
                           "MERCHANT_KEY": MERCHANT_KEY,
                           "txnid": txnid,
                           "hash_string": hash_string,
                           "action": "."})

#===================THIS CODE IS GETING FROM PAYUMONEY SITE===============================
@csrf_protect
@csrf_exempt
def success(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "GQs7yium"
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ", txnid)
        print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")

    cur_date = datetime.date.today()
    next_month_date = cur_date+timedelta(days=30)  #create expire date

    manager = Manager.objects.filter(email=email).first()

    #create Subscription object
    subobj = Subscription(plan=productinfo, date=cur_date,
                          price=float(amount),expireDate=next_month_date,transactionId=txnid)
    subobj.mangerref=manager
    subobj.save()       #save Subscription

    return render(request, 'sucess.html',
                  {"manager": manager,
                   "txnid": txnid,
                   "status": status,
                   "amount": amount})

#===================THIS CODE IS GETING FROM PAYUMONEY SITE===============================
@csrf_protect
@csrf_exempt
def failure(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = ""
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ", txnid)
        print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")

    #create manager object
    manager = Manager(fName=firstname,email=email)
    return render(request, 'Failure.html',
                    {"manager": manager,
                     "txnid": txnid,
                     "status": status,
                     "amount": amount})
    #return render_to_response("Failure.html", RequestContext(request, c))


