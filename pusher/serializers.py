from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
import datetime


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')
 

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('password', 'first_name', 'last_name', 'email',)
#         write_only_fields = ('password',)
#         read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)
 
#     def restore_object(self, attrs, instance=None):
#         # call set_password on user object. Without this
#         # the password will be stored in plain text.
#         user = super(UserSerializer, self).restore_object(attrs, instance)
#         user.set_password(attrs['password'])
#         return user


# class UserDataSerializer(serializers.Serializer):
#     userID = serializers.IntegerField(read_only=True)
#     deviceID = serializers.CharField(required=True, allow_blank=False, max_length=255)

#     def create(self, validated_data):
#         return UserData.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.deviceID = validated_data.get('deviceID', instance.deviceID)
#         instance.save()
#         return instance
#         


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #deviceId = serializers.PrimaryKeyRelatedField(many=False, queryset=UserDevice.objects.all())
    #device = serializers.SerializerMethodField('get_deviceId')
    #deviceId = CharField(source='get_absolute_url')
    deviceId = serializers.CharField(source='deviceInfo.deviceId')

    #device = UserDeviceSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'deviceId')

    def update(self, instance, validated_data):
        newDeviceId = validated_data.pop('deviceInfo').pop('deviceId')
        device = instance.device
        device.deviceId = newDeviceId
        device.save()
        return super(UserSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        device_data = validated_data.pop('device').pop('deviceId')

class registerUserSerializer(serializers.HyperlinkedModelSerializer):
    deviceId = serializers.CharField(source='deviceInfo.deviceId')
    class Meta:
        model = User
        fields = ('username', 'password', 'deviceId')
    def create(self, validated_data):
        device_data = validated_data.pop('deviceInfo').pop('deviceId')
        

    def validate(self, data):
        if set(['username', 'password', 'deviceInfo']).issubset(data):
            return data
        else:
            raise serializers.ValidationError("All field must be present")



class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class NotificationDataSerializer(serializers.ModelSerializer):
    #deviceId = serializers.CharField(source='Participant.deviceId')
    owner = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='deviceId',
        queryset=Participant.objects.all()
    )
    #deviceId = serializers.CharField(max_length=255, allow_blank=False, read_only=True)

    class Meta:
        model = NotificationData
        fields = ('owner','received','responded', 'location')
        extra_kwargs = {
            'received': {
                'format':['%Y-%m-%d %H:%M:%S'],
                'input_formats':['%Y-%m-%d %H:%M:%S']
            },
            'responded': {
                'format':['%Y-%m-%d %H:%M:%S'],
                'input_formats':['%Y-%m-%d %H:%M:%S']
            }
        }        

    # def create(self, validated_data):
    #     import pdb;pdb.set_trace()
    #     ide = validated_data.pop('deviceId')
    #     participant = Participant.objects.get(deviceId=ide)
    #     notificationData = NotificationData(
    #         owner=participant,
    #         received=validated_data['received'],
    #         responded=validated_data['responded'],
    #         location=validated_data['location']
    #     )
    #     notificationData.save()
    #     return notificationData

class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    deviceId = serializers.CharField(source='GCMDevice.registration_id')
    class Meta:
        model = Participant
        fields = ('age', 'gender', 'occupation', 'deviceId')
    def create(self, validated_data):
        device_data = validated_data.pop('GCMDevice').pop('registration_id')
        instance = Participant(**validated_data)
        instance.save()
        return instance
        

    def validate(self, data):
        print(data)
        if set(['age', 'gender', 'occupation', 'GCMDevice']).issubset(data):
            return data
        else:
            raise serializers.ValidationError("All field must be present")

class DataSerializer(serializers.HyperlinkedModelSerializer):
    messageId = serializers.IntegerField()
    class Meta:
        model = NotificationData
        fields = ('received','responded', 'busyness', 'messageId', 'stress')
        extra_kwargs = {
            'received': {
                'format':['%Y-%m-%d %H:%M:%S'],
                'input_formats':['%Y-%m-%d %H:%M:%S']
            },
            'responded': {
                'format':['%Y-%m-%d %H:%M:%S'],
                'input_formats':['%Y-%m-%d %H:%M:%S']
            }
        }    
    def create(self, validated_data):
        messageId = validated_data.pop('messageId')
        instance = NotificationData(**validated_data)
        instance.save()
        return instance
        
    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.received = validated_data.get('received', instance.received)
        instance.responded = validated_data.get('responded', instance.responded)
        instance.server_recieved = datetime.datetime.now()
        instance.busyness = validated_data.get('busyness', instance.busyness)
        instance.stress = validated_data.get('stress', instance.stress)
        instance.save()
        return instance

    def validate(self, data):
        print(data)
        if set(['received','responded', 'busyness', 'messageId', 'stress']).issubset(data):
            return data
        else:
            raise serializers.ValidationError("All field must be present")