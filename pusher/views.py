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
from .forms import *
import datetime


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

from push_notifications.models import GCMDevice

@csrf_exempt
def register_participant(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serialized = RegisterSerializer(data=data)
        if serialized.is_valid():
            deviceId = serialized.initial_data['deviceId']
            try:
                GCMDevice.objects.get(registration_id=deviceId)
                return HttpResponse("user with device already exists", status=status.HTTP_400_BAD_REQUEST)
            except GCMDevice.DoesNotExist:
                device = GCMDevice(registration_id=deviceId)
                device.save()
                participant = serialized.save(device=device)
                return JsonResponse({'message': "participant registered"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serialized.errors, status=400)
    return JsonResponse({'error': "can only accept POST request"}, status=400)

@csrf_exempt
def save_notification_data(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serialized = DataSerializer(data=data)
        #serialized = NotificationDataSerializer(data=data)
        if serialized.is_valid():
            deviceId = serialized.initial_data['deviceId']
            try:
                participant = Participant.objects.get(device__registration_id=deviceId)
                serialized.save(owner=participant)
                return JsonResponse({'message': "data registered"}, status=status.HTTP_201_CREATED)
            except Participant.DoesNotExist:
                return JsonResponse({'error': "no with requested device"}, status=status.HTTP_400_BAD_REQUEST)
                
        return JsonResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': "can only accept POST request"}, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Max


@login_required(login_url='/login')
def list_participants(request):
    participants = Participant.objects.annotate(latest_order=Max('notificationdata__responded')).order_by('latest_order')
    #participants = Participant.objects.all().prefetch_related('notificationdata_set')
    if request.method == "POST":
        #import pdb;pdb.set_trace()
        formset = ParticipantFormSet(request.POST, queryset = participants)
        if formset.is_valid():
            participant_to_push = []
            for form in formset.forms:
                if form.cleaned_data['push']:
                    participant_to_push.append(form.instance)
            for participant in participant_to_push:
                import pdb;pdb.set_trace()
                data = NotificationData(owner=participant, server_sent=datetime.datetime.now())
                data.save()
                device = participant.device
                device.send_message(None, extra={"messegeId": str(data.pk)})
    else:
        formset = ParticipantFormSet(queryset=participants)
    return render(request, 'pusher/participants.html', {"formset":formset, "ziped_data":zip(formset.forms,participants)})

@login_required(login_url='/login')
def list_participant_data(request, participant_id):
    participant = Participant.objects.get(pk=participant_id)
    notificationDatas = participant.notificationdata_set.all().order_by("-received")

    return render(request, 'pusher/participant_data.html', {"notificationDatas":notificationDatas,})

@login_required(login_url='/login')
def list_all_data(request):
    notificationDatas = NotificationData.objects.all()
    return render(request, 'pusher/participant_data.html', {"notificationDatas":notificationDatas,})