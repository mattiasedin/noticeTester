from django.conf.urls import url
from django.contrib import admin
from . import views
from rest_framework.authtoken import views as rest_views


urlpatterns = [
    #url(r'^users/', views.user_list),
    #url(r'^register/', views.create_auth),
    #url(r'^token-auth/', rest_views.obtain_auth_token),
    url(r'^api/register/', views.register_participant),
    url(r'^api/notification/', views.save_notification_data),
    url(r'^participants/$', views.list_participants),
    url(r'^participants/(?P<participant_id>\d+)/$', views.list_participant_data, name="participant_data"),
]


 

