from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import *
from .serializers import *


@api_view(['GET'])
#@authentication_classes((SessionAuthentication, BasicAuthentication))
#@permission_classes((IsAuthenticated,))
def user_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }

    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

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
                    user = User.objects.create_user(username=serialized.initial_data['username'],
                        password=serialized.initial_data['password']
                    )
                    userDevice = UserDevice(owner=user, deviceId=deviceId)

                    userDevice.save()
                    return JsonResponse({'message': "user successfully created"}, status=status.HTTP_201_CREATED)
                return JsonResponse({'error': "an error has occured"}, status=status.HTTP_400_BAD_REQUEST)
                #return JsonResponse(token, status=status.HTTP_201_CREATED)
                #return HttpResponse("user created", status=status.HTTP_201_CREATED)
                #return Response("user created", status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return JsonResponse({"error": e.message}, status=400)
                #return HttpResponse(e.message, status=status.HTTP_400_BAD_REQUEST)
                #return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(serialized.errors, status=400)
            #return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
            #return HttpResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': "an error has occured"}, status=400)
        #return Response("an error has occured", status=status.HTTP_400_BAD_REQUEST)
        #return HttpResponse("an error has occured", status=status.HTTP_400_BAD_REQUEST)
        #
@csrf_exempt
def register_participant(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serialized = ParticipantSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return JsonResponse({'message': "participant registered"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serialized.errors, status=400)
    return JsonResponse({'error': "can only accept POST request"}, status=400)

@csrf_exempt
def save_notification_data(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serialized = NotificationDataSerializer(data=data)
        import pdb;pdb.set_trace()
        if serialized.is_valid():
            serialized.save()
            return JsonResponse({'message': "data registered"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serialized.errors, status=400)
    return JsonResponse({'error': "can only accept POST request"}, status=400)

@login_required(login_url='/login')
def list_participants(request):
    participants = Participant.objects.all()
    return render(request, 'pusher/participants.html', {"participants":participants,})

@login_required(login_url='/login')
def list_participant_data(request, participant_id):
    participant = Participant.objects.get(pk=participant_id)
    notificationDatas = participant.notificationdata_set.all().order_by("received")

    return render(request, 'pusher/participant_data.html', {"notificationDatas":notificationDatas,})