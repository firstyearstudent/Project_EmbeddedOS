import sys
import dbus

if len(sys.argv) != 2:
    print("Usage: python3 usb_unmount.py <devname>")
    print("Chỉ dùng cho thiết bị storage, ví dụ: python3 usb_unmount.py /dev/sda1")
    sys.exit(1)

devname = sys.argv[1]
if not devname.startswith("/dev/"):
    print("Chỉ unmount được thiết bị storage (devname phải bắt đầu bằng /dev/)")
    sys.exit(1)

bus = dbus.SystemBus()
usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
result = usb_manager.UnmountDevice(devname, dbus_interface='org.example.USBManager')
print("Unmount thành công!" if result else "Unmount thất bại!")