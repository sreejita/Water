"""cloudmatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Jul 17 Login Change
from django.views.generic import RedirectView

from wisconsin import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name ='index'),
    url(r'^lake_to_site/(?P<id>.+)/', views.lake_to_site, name ='lake_to_site'),
    url(r'^site_to_lake/', views.site_to_lake, name ='site_to_lake'),
    url(r'^waterbodies/(?P<page>\d+)/', views.waterbodies, name ='waterbodies'),
    url(r'^lake/(?P<id>.+)/', views.lake_detail, name ='lake_detail'),
    url(r'^sites/', views.sites, name ='sites'),
    url(r'^site/(?P<id>.+)/', views.site_detail, name ='site_detail'),
    url(r'^bbs/', views.bb, name ='bbs'),
    url(r'^bb/(?P<id>.+)/', views.bb_detail, name ='bb_detail'),
    # July 17 Login Change
    #url(r'^frontend/', include('frontend.urls',namespace='frontend',app_name='frontend')),
    #url(r'^$', RedirectView.as_view(permanent=False, url='/frontend/ulogin/')),
    #url(r'^', include('frontend.urls')),
    # url(r'^frontend/', include('frontend.urls')),
    # July 17 End


    # url(r'^accounts/login/$', login, {'template_name': 'admin/login.html'}, name='login'),
    # url(r'^accounts/logout/$', logout, name='logout'),
    # url(r'^', include('frontend.urls')),
    # url(r'^login/$', login, {'template_name': 'login.html', 'authentication_form': LoginForm}),
    # url(r'^logout/$', logout, {'next_page': '/login'}),
]

urlpatterns += staticfiles_urlpatterns()
