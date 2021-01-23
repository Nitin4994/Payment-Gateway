from django.contrib import admin
from django.urls import path,include

from django.conf.urls import url
from subscription.views import paymentgateway,success,failure
urlpatterns = [
    path('paymentgateway/', paymentgateway.as_view()),  #go to payment gateway
    path('Success/', success),      #after success payment
    path('Failure/', failure),      #after failure
]




