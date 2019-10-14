from django.conf.urls import url, include
from authentication.views import signup, login, test, logout, social_login

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', login, name='login'),
    url(r'^test/$', test, name='test'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^social-login/$',social_login, name='social_login')
]