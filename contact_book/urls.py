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

from storage.views import ShowPeopleView, AddPersonView, ShowPersonView, ModifyPerson, AddAddress, AddNumber, AddEmail, ModifyAddress\
    , ModifyNumber, ModifyEmail, DeletePerson, ShowGroupsView, AddMembers, AddToGroups, DeleteMember, ModifyGroup\
    , DeleteGroup, ShowGroup, WelcomeView, LoginView, RegisterView, AddAddressView, AddContactsView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^modify/(?P<my_id>\d+)/$', ModifyPerson.as_view()),
    url(r'^delete/(?P<my_id>\d+)/$', DeletePerson.as_view()),
    url(r'^(?P<my_id>\d+)/addAddress$', AddAddress.as_view()),
    url(r'^(?P<my_id>\d+)/addNumber$', AddNumber.as_view()),
    url(r'^(?P<my_id>\d+)/addEmail$', AddEmail.as_view()),
    url(r'^(?P<my_id>\d+)/modifyAddress$', ModifyAddress.as_view()),
    url(r'^(?P<my_id>\d+)/modifyNumber$', ModifyNumber.as_view()),
    url(r'^(?P<my_id>\d+)/modifyEmail$', ModifyEmail.as_view()),
    url(r'^group/(?P<group_id>\d+)$', ShowGroup.as_view()),
    url(r'^groups/addMembers/(?P<my_id>\d+)$', AddMembers.as_view()),
    url(r'^groups/addToGroups/(?P<my_id>\d+)$', AddToGroups.as_view()),
    url(r'^groups/deleteMember/(?P<group_id>\d+)/(?P<member_id>\d+)$', DeleteMember.as_view()),
    url(r'^groups/modify/(?P<group_id>\d+)/$', ModifyGroup.as_view()),
    url(r'^groups/delete/(?P<group_id>\d+)/$', DeleteGroup.as_view()),



    url(r'^welcome/$', WelcomeView.as_view(), name='welcome'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),


    url(r'^show/people$', ShowPeopleView.as_view(), name='show_people'),
    url(r'^show/(?P<person_id>\d+)/$', ShowPersonView.as_view(), name='show_person'),

    url(r'^new/person$', AddPersonView.as_view(), name='add_person'),
    url(r'^new/address/(?P<person_id>\d+)$', AddAddressView.as_view(), name='add_address'),
    url(r'^new/contacts/(?P<person_id>\d+)$', AddContactsView.as_view(), name='add_contacts'),

    url(r'^groups/$', ShowGroupsView.as_view(), name='show_groups'),

]




