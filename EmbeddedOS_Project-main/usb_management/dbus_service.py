"""
D-Bus service cho quản lý USB.
Cung cấp các method: ListDevices, MountDevice, UnmountDevice, GetStatus, SendEvent.
"""

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

# Giả sử bạn có các hàm hoặc class quản lý thiết bị USB ở nơi khác
# Ở đây sẽ dùng biến giả lập để minh họa

class USBManagerService(dbus.service.Object):
    """
    D-Bus service cho quản lý USB.
    """

    def __init__(self, bus, object_path='/org/example/USBManager'):
        super().__init__(bus, object_path)
        # Danh sách thiết bị giả lập
        self.device_list = [
            {"id": "usb1", "name": "USB Flash", "status": "mounted"},
            {"id": "usb2", "name": "USB Audio", "status": "unmounted"},
        ]

    @dbus.service.method("org.example.USBManager",
                         in_signature='', out_signature='a{sa{sv}}')
    def ListDevices(self):
        """
        Trả về danh sách thiết bị USB hiện tại.
        """
        # Trả về danh sách thiết bị dạng list các dict
        return self.device_list

    @dbus.service.method("org.example.USBManager",
                         in_signature='s', out_signature='b')
    def MountDevice(self, device_id):
        """
        Mount thiết bị USB theo device_id.
        """
        for dev in self.device_list:
            if dev["id"] == device_id:
                dev["status"] = "mounted"
                return True
        return False

    @dbus.service.method("org.example.USBManager",
                         in_signature='s', out_signature='b')
    def UnmountDevice(self, device_id):
        """
        Unmount thiết bị USB theo device_id.
        """
        for dev in self.device_list:
            if dev["id"] == device_id:
                dev["status"] = "unmounted"
                return True
        return False

    @dbus.service.method("org.example.USBManager",
                         in_signature='s', out_signature='s')
    def GetStatus(self, device_id):
        """
        Lấy trạng thái thiết bị USB.
        """
        for dev in self.device_list:
            if dev["id"] == device_id:
                return dev["status"]
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
    print("USBManagerService D-Bus đang chạy...")
    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()