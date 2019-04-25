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

from storage.views import ShowPeopleView, AddPersonView, ShowPersonView, UpdatePersonView, DeletePersonView, \
    ShowGroupsView, AddMembers, AddToGroupsView, DeleteMember, ModifyGroup, DeleteGroup, ShowGroupView, WelcomeView, \
    LoginView, LogoutView, RegisterView, AddAddressView, AddContactsView, EditPersonView

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^groups/addMembers/(?P<my_id>\d+)$', AddMembers.as_view()),
    url(r'^groups/deleteMember/(?P<group_id>\d+)/(?P<member_id>\d+)$', DeleteMember.as_view()),
    url(r'^groups/modify/(?P<group_id>\d+)/$', ModifyGroup.as_view()),
    url(r'^groups/delete/(?P<group_id>\d+)/$', DeleteGroup.as_view()),



    url(r'^$', WelcomeView.as_view(), name='welcome'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^show/people$', ShowPeopleView.as_view(), name='show_people'),
    url(r'^show/(?P<pk>\d+)/$', ShowPersonView.as_view(), name='show_person'),
    # url(r'^update/(?P<pk>\d+)/$', UpdatePersonView.as_view(), name='update_person'),
    url(r'^update/(?P<pk>\d+)/$', EditPersonView.as_view(), name='update_person'),

    url(r'^delete/(?P<pk>\d+)/$', DeletePersonView.as_view(), name='delete_person'),

    url(r'^new/person$', AddPersonView.as_view(), name='add_person'),
    url(r'^new/address/(?P<person_id>\d+)$', AddAddressView.as_view(), name='add_address'),
    url(r'^new/contacts/(?P<person_id>\d+)$', AddContactsView.as_view(), name='add_contacts'),


    url(r'^show/groups/$', ShowGroupsView.as_view(), name='show_groups'),
    url(r'^group/(?P<group_id>\d+)$', ShowGroupView.as_view(), name='show_group'),
    url(r'^group/addperson/(?P<person_id>\d+)$', AddToGroupsView.as_view(), name='add_to_groups'),


]




