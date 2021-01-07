from django.conf.urls import url
from django.urls import include, path
from items.views import user_login

urlpatterns = [
    path("accounts/login/", user_login, name='user-login'),
]