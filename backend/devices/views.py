from rest_framework import generics
from rest_framework import status
from .serializers import DeviceSerializer
from django.views.generic.base import View
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Device
from scapy.all import ARP, Ether, srp
from rest_framework.views import APIView
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceDeleteView(generics.DestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceUpdateView(generics.UpdateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

def get_devices(request):
    devices = Device.objects.all()
    device_list = []
    for device in devices:
        device_data = {
            'id': device.id,
            'device_name': device.device_name,
            'device_type': device.device_type,
            'ip_address': device.ip_address,
            'mac_address': device.mac_address,
            'department': device.department,
            'building': device.building,
            'floor': device.floor,
        }
        device_list.append(device_data)

    return JsonResponse(device_list, safe=False)
class NetworkScanView(APIView):
    def post(self, request, format=None):
        # Retrieve the target IP range from the request data
        target_ip_range = request.data.get('ip_range')

        # Create an ARP request packet
        arp = ARP(pdst=target_ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        # Send the packet and capture the response
        result = srp(packet, timeout=3, verbose=0)[0]

        # Retrieve existing devices in the database
        existing_devices = Device.objects.filter(ip_address__in=[received.psrc for _, received in result])

        # Create a dictionary to map existing devices by IP address
        existing_devices_map = {device.ip_address: device for device in existing_devices}

        # Update device information based on the response
        devices_to_create = []
        devices_to_update = []
        for sent, received in result:  
            ip_address = received.psrc
            mac_address = received.hwsrc

            if ip_address in existing_devices_map:
                device = existing_devices_map[ip_address]

                # Update device information if there are any changes
                if device.mac_address != mac_address:
                    device.mac_address = mac_address
                    devices_to_update.append(device)

                # Update device status
                device.is_online = True
                devices_to_update.append(device)
            else:
                # Create a new device if it doesn't exist
                device = Device(
                    device_name='Unknown',
                    device_type='Unknown',
                    ip_address=ip_address,
                    mac_address=mac_address,
                    department='Unknown',
                    building='Unknown',
                    floor='Unknown',
                    is_online=True
                )
                devices_to_create.append(device)

        # Bulk update existing devices
        Device.objects.bulk_update(devices_to_update, ['mac_address', 'is_online'])

        # Bulk create new devices
        Device.objects.bulk_create(devices_to_create)

        # Return a JSON response indicating the scan was successful
        return Response({'message': 'Network scan completed.'}, status=status.HTTP_200_OK)

    class DeviceUpdateDestroyView(APIView):
        def put(self, request, pk, format=None):
            device = self.get_object(pk)
            serializer = DeviceSerializer(device, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, pk, format=None):
            device = self.get_object(pk)
            device.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)