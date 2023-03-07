from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PiDevice,SocketDeviceIds
from django.contrib import messages
import json
# messages.add_message(request, messages.INFO, 'Hello world.')
class SocketDeviceIdsAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id','is_approved','connections_count','date_added',)
    list_filter = ('device_id','is_approved','connections_count','date_added',)
    actions = ['approve_device']
    def approve_device(self, request, queryset):
        for device in queryset:
            device.is_approved = True
            device.save()
            messages.add_message(request, messages.INFO, 'Approved %s (%d)' % (device.device_id, device.id))
admin.site.register(SocketDeviceIds,SocketDeviceIdsAdmin)
# Register your models here.
class PiDeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'name','cec_hdmi_status','is_socket_connected_live','humanize_socket_status_updated_ago','device_id',)
    list_filter = ('device_id','name','cec_hdmi_status','socket_status_updated',)
    actions = ['reboot_device','hdmi_cec_off','hdmi_cec_on','relaunch_kiosk_browser',]
    
    def reboot_device(self, request, queryset):
        for pi_device in queryset:
            res = pi_device.send_reboot()
            if res:
                messages.add_message(request, messages.INFO, 'Rebooted %s (%d)' % (pi_device.name, pi_device.id))
            else:
                messages.add_message(request, messages.WARNING, 'Device %s (%d) is not connected' % (pi_device.name, pi_device.id))
    reboot_device.short_description = "Reboot device"
    
    def hdmi_cec_off(self, request, queryset):
        for pi_device in queryset:
            res = pi_device.send_hdmi_cec_off()
            if res:
                messages.add_message(request, messages.INFO, 'HDMI CEC turned off for %s (%d)' % (pi_device.name, pi_device.id))
            else:
                messages.add_message(request, messages.WARNING, 'Device %s (%d) is not connected' % (pi_device.name, pi_device.id))
    hdmi_cec_off.short_description = "HDMI CEC off"
    
    def hdmi_cec_on(self, request, queryset):
        for pi_device in queryset:
            res = pi_device.send_hdmi_cec_on()
            if res:
                messages.add_message(request, messages.INFO, 'HDMI CEC turned on for %s (%d)' % (pi_device.name, pi_device.id))
            else:
                messages.add_message(request, messages.WARNING, 'Device %s (%d) is not connected' % (pi_device.name, pi_device.id))
    hdmi_cec_on.short_description = "HDMI CEC on"
    
    def relaunch_kiosk_browser(self, request, queryset):
        for pi_device in queryset:
            res = pi_device.send_relaunch_kiosk_browser()
            if res:
                messages.add_message(request, messages.INFO, 'Relaunched kiosk browser for %s (%d)' % (pi_device.name, pi_device.id))
            else:
                messages.add_message(request, messages.WARNING, 'Device %s (%d) is not connected' % (pi_device.name, pi_device.id))
    relaunch_kiosk_browser.short_description = "Relaunch kiosk browser"
admin.site.register(PiDevice, PiDeviceAdmin)
