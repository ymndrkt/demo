from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id',
                  'device_name',
                  'device_type',
                  'ip_address',
                  'mac_address',
                  'department',
                  'building',
                  'floor',
                  'is_online'
                  )
