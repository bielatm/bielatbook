from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.register, name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^home/$', views.home_page, name='home_page'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
]
