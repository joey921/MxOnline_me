#coding: utf-8
"""MxOnline URL Configuration
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
import xadmin
from django.views.generic import TemplateView
from django.views.static  import serve


from users.views import  index
from users.views import LoginView,RegisterView, LogoutView,AciveUserView, ForgetPwdView, ResetView, ModifyPwdView
from organization.views import OrgView
from MxOnline.settings  import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # url(r'^$',TemplateView.as_view(template_name='index.html'),name='index'),
    # url('^login/$', LoginView.as_view(), name="login"),
    url(r'^$', index, name='index'),
    url(r'^index/$', index, name='index'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^active/(?P<active_code>.*)',AciveUserView.as_view(),name='user_active'),
    url(r'^reset/(?P<active_code>.*)',ResetView.as_view(),name='reset_pwd'),
    url(r'^modify_pwd/$',ModifyPwdView.as_view(),name='modify_pwd'),
    url(r'^forget/$',ForgetPwdView.as_view(),name='forget_pwd'),

    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace='org')),

    # 课程相关url配置
    url(r'^course/', include('courses.urls', namespace="course")),


    url(r'^media/(?P<path>.*)$',serve ,{'document_root': MEDIA_ROOT}),  #处理静态文件的路由


]
