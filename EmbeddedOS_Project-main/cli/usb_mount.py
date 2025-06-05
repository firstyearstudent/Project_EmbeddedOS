import sys
import dbus

if len(sys.argv) != 2:
    print("Usage: python3 usb-mount.py <devpath>")
    sys.exit(1)

devpath = sys.argv[1]
bus = dbus.SystemBus()
usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
result = usb_manager.MountDevice(devpath, dbus_interface='org.example.USBManager')
print("Mount thành công!" if result else "Mount thất bại!")