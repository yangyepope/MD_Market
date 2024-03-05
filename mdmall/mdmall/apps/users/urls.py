from django.urls import path, re_path

from . import views
from . import views

urlpatterns = [
    re_path(r'^register/$', views.UserView.as_view())
]
