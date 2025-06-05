import sys
import dbus

if len(sys.argv) != 2:
    print("Usage: python3 usb-unmount.py <devpath>")
    sys.exit(1)

devpath = sys.argv[1]
bus = dbus.SystemBus()
usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
result = usb_manager.UnmountDevice(devpath, dbus_interface='org.example.USBManager')
print("Unmount thành công!" if result else "Unmount thất bại!")