from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import PiDevice
from django.http import JsonResponse
# Create your views here.
@csrf_exempt
def command_view(request):
    if request.method == "POST":
        print(request.POST)
        # data = {'command': 'reboot', 'device_id': self.device_id}
        command = request.POST.get('command')
        device_id = request.POST.get('device_id')
        res = None
        if command == 'reboot':
            pi_device = PiDevice.objects.get(device_id=device_id)
            res = pi_device.send_reboot()
        elif command == 'set_tv_url':
            pi_device = PiDevice.objects.get(device_id=device_id)
            url = request.POST.get('url')
            res = pi_device.send_set_tv_url(url)
        elif command == 'hdmi_cec_off':
            pi_device = PiDevice.objects.get(device_id=device_id)
            res = pi_device.send_hdmi_cec_off()
        elif command == 'hdmi_cec_on':
            pi_device = PiDevice.objects.get(device_id=device_id)
            res = pi_device.send_hdmi_cec_on()
        elif command == 'relaunch_kiosk_browser':
            pi_device = PiDevice.objects.get(device_id=device_id)
            res = pi_device.send_relaunch_kiosk_browser()
        else:
            print('command not found')
            res = 'command not found'
        return JsonResponse({'res':res})