import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
import pyudev
import subprocess
import os

class USBManagerService(dbus.service.Object):
    """
    D-Bus service cho quản lý USB thực tế.
    """

    def __init__(self, bus, object_path='/org/example/USBManager'):
        super().__init__(bus, object_path)
        self.context = pyudev.Context()

    @dbus.service.method("org.example.USBManager",
                         in_signature='', out_signature='aa{sv}')
    def ListDevices(self):
        """
        Trả về danh sách thiết bị USB hiện tại.
        """
        devices = []
        for device in self.context.list_devices(subsystem='usb', DEVTYPE='usb_device'):
            dev_info = {
                "id": device.get('DEVPATH', ''),
                "vendor": device.get('ID_VENDOR', ''),
                "product": device.get('ID_MODEL', ''),
                "serial": device.get('ID_SERIAL_SHORT', ''),
                "class": device.get('ID_USB_CLASS', ''),
                "busnum": device.get('BUSNUM', ''),
                "devnum": device.get('DEVNUM', ''),
                "status": self._get_status(device)
            }
            devices.append(dev_info)
        return devices

    def _get_status(self, device):
        # Nếu là thiết bị lưu trữ, kiểm tra đã mount chưa
        if device.get('ID_USB_DRIVER') == 'usb-storage':
            devname = self._find_block_device(device)
            if devname and self._is_mounted(devname):
                return "mounted"
            else:
                return "unmounted"
        return "connected"

    def _find_block_device(self, device):
        # Tìm block device (vd: /dev/sda1) tương ứng với thiết bị USB
        for child in device.children:
            if child.subsystem == 'block':
                return '/dev/' + os.path.basename(child.device_node)
        return None

    def _is_mounted(self, devname):
        with open('/proc/mounts') as f:
            for line in f:
                if devname in line:
                    return True
        return False

    @dbus.service.method("org.example.USBManager",
                         in_signature='s', out_signature='b')
    def MountDevice(self, devpath):
        """
        Mount thiết bị USB lưu trữ theo devpath.
        """
        device = pyudev.Device.from_device_file(self.context, devpath)
        devname = self._find_block_device(device)
        if devname:
            mount_point = f"/media/{os.path.basename(devname)}"
            os.makedirs(mount_point, exist_ok=True)
            try:
                subprocess.check_call(['mount', devname, mount_point])
                return True
            except Exception as e:
                print(f"Mount lỗi: {e}")
        return False

    @dbus.service.method("org.example.USBManager",
                         in_signature='s', out_signature='b')
    def UnmountDevice(self, devpath):
        """
        Unmount thiết bị USB lưu trữ theo devpath.
        """
        device = pyudev.Device.from_device_file(self.context, devpath)
        devname = self._find_block_device(device)
        if devname:
            try:
                subprocess.check_call(['umount', devname])
                return True
            except Exception as e:
                print(f"Unmount lỗi: {e}")
        return False

    @dbus.service.method("org.example.USBManager",
                         in_signature='s', out_signature='s')
    def GetStatus(self, devpath):
        """
        Lấy trạng thái thiết bị USB.
        """
        try:
            device = pyudev.Device.from_device_file(self.context, devpath)
            return self._get_status(device)
        except Exception:
            return "unknown"

    @dbus.service.signal("org.example.USBManager",
                         signature='ss')
    def SendEvent(self, event_type, data):
        """
        Gửi sự kiện tới client (signal).
        """
        pass  # Signal sẽ được gửi khi gọi hàm này

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    name = dbus.service.BusName("org.example.USBManager", bus)
    service = USBManagerService(bus)
    print("USBManagerService D-Bus thực tế đang chạy...")
    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()