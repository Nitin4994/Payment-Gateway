from django.contrib import admin
from django.urls import path,include

#from user.views import login,register,register_save,login_success,home_page,user_loginout
from manager.views import *
urlpatterns = [
    path('', login),    #go to main page--login
    path('register/', register),  #go to registration page
    path('register/save/', RegisterSave.as_view()),  #after registration--save registration in DB
    path('login/', LoginSuccess.as_view()),     #after correct email and password-go to home page
    path('logout/', user_loginout),     #after logout
    path('home/', home_page),           #go to home page
    path('yourplans/', your_plans),     #go to your plan tab
    path('cancel/<int:sid>', your_plans_cancel),    #go to cancel subscription
    path('resume/<int:sid>', your_plans_resume),    #go to resume subscription
]




