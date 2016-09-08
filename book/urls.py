from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.register, name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^home/$', views.home_page, name='home_page'),
    url(r'^edit-profile/$', views.edit_profile, name='edit_profile'),
    url(r'^find-friends/$', views.find_friends, name='find_friends'),
    url(r'^accept-invitations/$', views.accept_invitations, name='accept_invitations'),
    url(r'^friends/$', views.friends_list, name='friends_list'),
    url(r'^messages/$', views.messages_list, name='messages_list'),
]
