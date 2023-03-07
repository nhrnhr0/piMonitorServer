from django.db import models
from django.utils import timezone
import humanize
from django.utils.safestring import mark_safe
import os


# from pi.storage import OverwriteStorage
# Create your models here.
def image_path(instance, filename):
    return os.path.join('last_images', str(instance.id), 'image.jpg')

class SocketDeviceIds(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    connections_count = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
class PiDevice(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    # remote_status = models.CharField(max_length=100, default='offline')
    # remote_status_updated = models.DateTimeField(null=True)
    # remote_last_image_url = models.CharField(max_length=100, blank=True, null=True)
    # I added blank True and null True
    remote_last_image = models.ImageField(upload_to=image_path, blank=True, null=True)  # , storage=OverwriteStorage())
    
    # is_socket_connected = models.BooleanField(default=False)
    socket_status_updated = models.DateTimeField(null=True)
    cec_hdmi_status = models.CharField(max_length=100, default='unknown')
    group_channel_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name or self.device_id

    def is_socket_connected_live(self):
        return self.group_channel_name is not None
    is_socket_connected_live.short_description = 'socket connected'
    is_socket_connected_live.boolean = True

    def send_reboot(self):
        try:
            if self.is_socket_connected_live():
                channel_name = self.group_channel_name
                from .consumers import send_reboot_to_channel
                send_reboot_to_channel(channel_name)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
    
    def send_hdmi_cec_off(self):
        try:
            if self.is_socket_connected_live():
                channel_name = self.group_channel_name
                from .consumers import send_hdmi_cec_off_to_channel
                send_hdmi_cec_off_to_channel(channel_name)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
    
    def send_hdmi_cec_on(self):
        try:
            if self.is_socket_connected_live():
                channel_name = self.group_channel_name
                from .consumers import send_hdmi_cec_on_to_channel
                send_hdmi_cec_on_to_channel(channel_name)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
    
    def send_relaunch_kiosk_browser(self):
        try:
            if self.is_socket_connected_live():
                channel_name = self.group_channel_name
                from .consumers import send_relaunch_kiosk_browser_to_channel
                send_relaunch_kiosk_browser_to_channel(channel_name)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def send_set_tv_url(self, url):
        try:
            if self.is_socket_connected_live():
                channel_name = self.group_channel_name
                from .consumers import send_set_tv_url_to_channel
                send_set_tv_url_to_channel(channel_name,url)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False



    def humanize_socket_status_updated_ago(self):
        # in hebrew
        return humanize.naturaltime(timezone.now() - self.socket_status_updated)

    humanize_socket_status_updated_ago.short_description = 'socket connection updated'

    def image_tag(self):
        if self.remote_last_image:
            return mark_safe(u'<img src="%s" width="150px" height="150px" />' % self.remote_last_image.url)
        else:
            return ''

