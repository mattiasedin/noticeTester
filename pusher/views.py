from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from django.views.defaults import bad_request

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
        try:
            messageId = data['messageId']
            instance = NotificationData.objects.get(pk=messageId)
            serialized = DataSerializer(instance, data=data)
            if serialized.is_valid():
                serialized.save()
                return JsonResponse({'message': "data registered"}, status=status.HTTP_201_CREATED)
            return JsonResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return JsonResponse({'error': "messageId not pressent"}, status=status.HTTP_400_BAD_REQUEST)
        except NotificationData.DoesNotExist:
            return JsonResponse({'error': "no message with given ID"}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': "can only accept POST request"}, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Max


@login_required(login_url='/login')
def list_participants(request):
    participants = Participant.objects.annotate(latest_order=Max('notificationdata__responded')).order_by('latest_order')
    #participants = Participant.objects.all().prefetch_related('notificationdata_set')
    if request.method == "POST":
        formset = ParticipantFormSet(request.POST, queryset = participants)
        if formset.is_valid():
            participant_to_push = []
            for form in formset.forms:
                if form.cleaned_data['push']:
                    participant_to_push.append(form.instance)
            for participant in participant_to_push:
                data = NotificationData(owner=participant, server_sent=datetime.datetime.now())
                data.save()
                device = participant.device
                device.send_message(None, extra={"messageId": str(data.pk)})
    else:
        formset = ParticipantFormSet(queryset=participants)
    nrMales = Participant.objects.filter(gender='M').count()
    nrWomans = participants.count() - nrMales
    nrStudents = Participant.objects.filter(occupation='S').count()
    nrEmployed = Participant.objects.filter(occupation='E').count()
    nrOther = participants.count() - nrStudents - nrEmployed
    
    return render(request, 'pusher/participants.html', {
        "formset":formset, 
        "ziped_data":zip(formset.forms,participants), 
        "nrMales":nrMales, 
        "nrWomans":nrWomans,
        "nrStudents":nrStudents,
        "nrEmployed":nrEmployed, 
        "nrOther":nrOther })

@login_required(login_url='/login')
def list_participant_data(request, participant_id):
    participant = Participant.objects.get(pk=participant_id)
    notificationDatas = participant.notificationdata_set.all().order_by("-received")

    return render(request, 'pusher/participant_data.html', {"notificationDatas":notificationDatas,})

@login_required(login_url='/login')
def list_all_data(request):
    notificationDatas = NotificationData.objects.all()
    return render(request, 'pusher/participant_data.html', {"notificationDatas":notificationDatas,})

@login_required(login_url='/login')
def list_occupation_data(request):
    occupation = request.GET.get('occupation', '')
    if occupation:
        notificationDatas = NotificationData.objects.filter(owner__occupation=occupation)
        return render(request, 'pusher/participant_data.html', {"notificationDatas":notificationDatas,})
    else:
        return bad_request(request, exception, template_name='400.html')
