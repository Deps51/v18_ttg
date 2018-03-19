from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import login, logout 

urlpatterns = [
    url(r'^$', views.check_logged_in, name='signup'),
    url(r'^thanks/', views.thanks, name='thanks'),
    url(r'^signin/', login, {"template_name":"signup/signin.html"}),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^myaccount/', views.myaccount, name='myaccount'),
     url(r'^remove/', views.remove, name='remove'),
    url(r'^logout/', logout, {"next_page":"../../accounts/signup"}),
    

]
