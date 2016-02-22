from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


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
        fields = ('username', 'email', 'password', 'deviceId')
    def create(self, validated_data):
        device_data = validated_data.pop('deviceInfo').pop('deviceId')
        

    def validate(self, data):
        if set(['username', 'email', 'password', 'deviceInfo']).issubset(data):
            return data
        else:
            raise serializers.ValidationError("All field must be present")