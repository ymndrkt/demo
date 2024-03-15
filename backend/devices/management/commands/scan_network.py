from django.core.management.base import BaseCommand
from ...models import Device
from scapy.all import ARP, Ether, srp

class Command(BaseCommand):
    help = 'Scans the network and updates device information'

    def handle(self, *args, **options):
        # Define the target IP range
        target_ip_range = '192.168.1.0/24'

        # Create an ARP request packet
        arp = ARP(pdst=target_ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        # Send the packet and capture the response
        result = srp(packet, timeout=3, verbose=0)[0]

        # Update device information based on the response
        devices = []
        for sent, received in result:
            devices.append({
                'device_name': 'Unknown',  # You can enhance this by performing further device identification
                'device_type': 'Unknown',
                'ip_address': received.psrc,
                'mac_address': received.hwsrc,
                'department': 'Unknown',
                'building': 'Unknown',
                'floor': 'Unknown',
                'is_online': True
            })

        # Bulk update or create devices in the database
        Device.objects.bulk_update_or_create(
            devices, keys=['ip_address'], fields=['mac_address', 'device_name', 'device_type', 'department', 'building', 'floor', 'is_online']
        )