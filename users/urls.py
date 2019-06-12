"""volunteerfind URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    url(r'^login/$', views.login_view),
    url(r'^leaderboard/$', views.leaderboard),
    url(r'^signup/$', views.signup_view),
    url(r'^logout/$', views.logout_view),
    url(r'^groups/create/$', views.create_group),
    url(r'^groups/addmember/$', views.add_member),
    url(r'^my-groups/(?P<username>[\w-]+)/$', views.my_groups, name="my_groups"),
    url(r'^groups/(?P<group_id>[\d]+)/$', views.view_group_profile, name="view_group_profile"),
    url(r'^(?P<username>[\w-]+)/$', views.view_user_profile, name="view_user_profile")
]
