"""
D-Bus service cho quản lý USB.
Cung cấp các method: ListDevices, MountDevice, UnmountDevice, GetStatus, SendEvent.
"""
import os
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
import pyudev
import subprocess

from usb_management.usb_ids_lookup import lookup_usb_name

USB_IDS_PATH = os.path.join(os.path.dirname(__file__), 'usb_ids.txt')

class USBManagerService(dbus.service.Object):
    def __init__(self, bus):
        super().__init__(bus, '/org/example/USBManager')
        self.context = pyudev.Context()

    @dbus.service.method("org.example.USBManager",
                         in_signature='', out_signature='aa{sv}')
    def ListDevices(self):
        devices = []
        for device in self.context.list_devices(subsystem='usb'):
            vendor_id = (device.get('ID_VENDOR_ID') or '').lower()
            product_id = (device.get('ID_MODEL_ID') or '').lower()
            vendor_name, product_name = lookup_usb_name(vendor_id, product_id, USB_IDS_PATH)
            # Tìm thiết bị block con (storage)
            devname = ""
            status = "connected"
            serial = str(device.get('ID_SERIAL_SHORT') or "")
            for child in device.children:
                if child.subsystem == 'block' and child.device_node:
                    devname = child.device_node
                    serial = str(child.get('ID_SERIAL_SHORT') or serial)
                    status = "mounted" if self.is_mounted(devname) else "unmounted"
                    break
            dev_info = {
                "vendor_id": vendor_id,
                "product_id": product_id,
                "vendor": vendor_name,
                "product": product_name,
                "status": status,
                "serial": serial,
                "devname": devname
            }
            devices.append(dev_info)
        return devices

    def is_mounted(self, devname):
        try:
            with open('/proc/mounts', 'r') as f:
                for line in f:
                    if devname in line:
                        return True
        except Exception:
            pass
        return False

    @dbus.service.method("org.example.USBManager",
                         in_signature='s', out_signature='b')
    def MountDevice(self, devname):
        mount_point = f"/mnt/usb_{os.path.basename(devname)}"
        try:
            subprocess.run(['mkdir', '-p', mount_point], check=True)
            subprocess.run(['mount', devname, mount_point], check=True)
            return True
        except Exception as e:
            print(f"Mount error: {e}")
            return False

    @dbus.service.method("org.example.USBManager",
                         in_signature='s', out_signature='b')
    def UnmountDevice(self, devname):
        try:
            subprocess.run(['umount', devname], check=True)
            return True
        except Exception as e:
            print(f"Unmount error: {e}")
            return False

    @dbus.service.method("org.example.USBManager",
                         in_signature='s', out_signature='s')
    def GetStatus(self, serial):
        """
        Lấy trạng thái thiết bị USB theo serial.
        """
        for device in self.context.list_devices(subsystem='block'):
            if (device.get('ID_SERIAL_SHORT') or "") == serial:
                devname = device.get('DEVNAME') or ""
                return "mounted" if devname and self.is_mounted(devname) else "unmounted"
        return "unknown"

    @dbus.service.signal("org.example.USBManager",
                         signature='ss')
    def SendEvent(self, event_type, data):
        pass  # Signal sẽ được gửi khi gọi hàm này

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    name = dbus.service.BusName("org.example.USBManager", bus)
    service = USBManagerService(bus)
    print("USBManagerService D-Bus đang chạy...")
    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()