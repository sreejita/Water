from django.conf.urls import url
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'frontend'
urlpatterns = [
    # ...
    # Login and home page related URLs
    url(r'^homepage/$', homepage, name='homepage'),
    url(r'^main_page/$', main_page, name='main_page'),
    url(r'^$', home, name='home'),
    url(r'^ulogin/$', auth_views.login, {'template_name': 'userreg/home.html'}, name='login'),
    url(r'^ulogout/$', auth_views.logout, {'template_name': 'userreg/logged_out.html'},  name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^index/$', index, name='index'),

    # Upload dataset URL
    url(r'upload_data/$', upload_data, name='upload_data'),

]
