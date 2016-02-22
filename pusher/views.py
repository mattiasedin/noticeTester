from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group

from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import jwt

from .models import *
from .serializers import *



# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer


# class UserView(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     model = User
 
#     def get_permissions(self):
#         # allow non-authenticated user to create via POST
#         return (AllowAny() if self.request.method == 'POST'
#                 else IsStaffOrTargetUser()),

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



@csrf_exempt
def user_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JSONResponse(serializer.data)

    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = UserSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JSONResponse(serializer.data, status=201)
    #     return JSONResponse(serializer.errors, status=400)

@csrf_exempt
#@api_view(['POST'])
def create_auth(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serialized = registerUserSerializer(data=data)
        if serialized.is_valid():
            try:
                deviceId = serialized.initial_data['deviceId']
                try:
                    user = UserDevice.objects.get(deviceId=deviceId)
                    return HttpResponse("user with device already exists", status=status.HTTP_400_BAD_REQUEST)
                except UserDevice.DoesNotExist:
                    user = User.objects.create_user(
                       serialized.initial_data['email'],
                       serialized.initial_data['username'],
                       serialized.initial_data['password']
                    )
                    userDevice = UserDevice(owner=user, deviceId=deviceId)
                    userDevice.save()
                return HttpResponse("user created", status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return HttpResponse(e.message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponse("an error has occured", status=status.HTTP_400_BAD_REQUEST)