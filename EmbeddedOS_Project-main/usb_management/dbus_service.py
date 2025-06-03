import dbus
@dbus.service.method('com.example.USBManager', out_signature='a{ss}')
def GetDeviceList(self):
    devices = {}
    
    # Thêm thông tin thiết bị thực tế của bạn vào đây
    devices["0781:5567"] = {
        "name": "SanDisk Cruzer Blade",
        "type": "storage",
        "serial": "4C530000110107116553",
        "mount_point": "/mnt/usb_sandisk"
    }
    
    # Thiết bị thứ 2
    devices["046d:c52b"] = {
        "name": "Logitech Unifying Receiver",
        "type": "hid",
        "driver": "usbhid"
    }
    
    return dbus.Dictionary(devices, signature='sv')