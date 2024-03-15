from django.urls import path
from .views import (DeviceListCreateView, DeviceRetrieveUpdateDestroyView, NetworkScanView, DeviceDeleteView,
    DeviceUpdateView,  )

urlpatterns = [
    path('devices/', DeviceListCreateView.as_view(), name='device-list-create'),
    path('devices/<int:pk>/', DeviceRetrieveUpdateDestroyView.as_view(), name='device-retrieve-update-destroy'),
    path('network-scan/', NetworkScanView.as_view(), name='network_scan'),  # Modified URL pattern
    path('devices/<int:pk>/delete/', DeviceDeleteView.as_view(), name='device-delete'),
    path('devices/<int:pk>/update/', DeviceUpdateView.as_view(), name='device-update'),
]