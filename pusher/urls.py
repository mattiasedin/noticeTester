from django.conf.urls import patterns, include, url
from . import views

from rest_framework import routers
from rest_framework_jwt import views as rest_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'accounts', views.UserView, 'list')


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^api-token-auth/', rest_views.obtain_jwt_token),
    url(r'^api-token-refresh/', rest_views.refresh_jwt_token),
]


 

