from django.db import models

class Device(models.Model):
    device_name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=100, default='null')
    ip_address = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    building = models.CharField(max_length=255)
    floor = models.CharField(max_length=255)
    is_online = models.BooleanField(default=False)