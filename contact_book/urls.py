"""contact_book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from storage.views import Home, AddPerson, ShowPerson, ModifyPerson, AddAddress, AddNumber, AddEmail, ModifyAddress\
    , ModifyNumber, ModifyEmail, DeletePerson, ShowGroups, AddMembers, AddToGroups, DeleteMember, ModifyGroup\
    , DeleteGroup

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', Home.as_view()),
    url(r'^new/$', AddPerson.as_view()),
    url(r'^show/(?P<my_id>\d+)/$', ShowPerson.as_view()),
    url(r'^modify/(?P<my_id>\d+)/$', ModifyPerson.as_view()),
    url(r'^delete/(?P<my_id>\d+)/$', DeletePerson.as_view()),
    url(r'^(?P<my_id>\d+)/addAddress$', AddAddress.as_view()),
    url(r'^(?P<my_id>\d+)/addNumber$', AddNumber.as_view()),
    url(r'^(?P<my_id>\d+)/addEmail$', AddEmail.as_view()),
    url(r'^(?P<my_id>\d+)/modifyAddress$', ModifyAddress.as_view()),
    url(r'^(?P<my_id>\d+)/modifyNumber$', ModifyNumber.as_view()),
    url(r'^(?P<my_id>\d+)/modifyEmail$', ModifyEmail.as_view()),
    url(r'^groups/$', ShowGroups.as_view()),
    url(r'^groups/addMembers/(?P<my_id>\d+)$', AddMembers.as_view()),
    url(r'^groups/addToGroups/(?P<my_id>\d+)$', AddToGroups.as_view()),
    url(r'^groups/deleteMember/(?P<group_id>\d+)/(?P<member_id>\d+)$', DeleteMember.as_view()),
    url(r'^groups/modify/(?P<group_id>\d+)/$', ModifyGroup.as_view()),
    url(r'^groups/delete/(?P<group_id>\d+)/$', DeleteGroup.as_view()),

]


