import sys
import dbus

if len(sys.argv) != 2:
    print("Usage: python3 usb_mount.py <devname>")
    print("Chỉ dùng cho thiết bị storage, ví dụ: python3 usb_mount.py /dev/sda1")
    sys.exit(1)

devname = sys.argv[1]
if not devname.startswith("/dev/"):
    print("Chỉ mount được thiết bị storage (devname phải bắt đầu bằng /dev/)")
    sys.exit(1)

bus = dbus.SystemBus()
usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
result = usb_manager.MountDevice(devname, dbus_interface='org.example.USBManager')
print("Mount thành công!" if result else "Mount thất bại!")