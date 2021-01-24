from django.contrib import admin
from django.urls import path,include

from django.conf.urls import url
from subscription.views import paymentgateway,success,failure
urlpatterns = [
    path('paymentgateway/', paymentgateway.as_view()),  #go to payment gateway
    path('Success/', success.as_view()),      #after success payment
    path('Failure/', failure.as_view()),      #after failure
]




