"""Group_Signature_mod URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from Groupsign import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^home/', views.home),
    url(r'^about/', views.about_view),
    url(r'^verify/', views.verify_view),
    url(r'^register/', views.register_user),
    url(r'^login/', views.user_login),
    url(r'^logout/', views.user_logout),
    url(r'^join/', views.user_join),
    url(r'^newmessege/', views.new_messege_view),
    url(r'^open/', views.open_view),
    url(r'^send_revocation_request/',views.revocation_request_view),
    url(r'^revoke/', views.revoke_list_add_view),
    url(r'^revokelist/', views.revoke_list_view),

]