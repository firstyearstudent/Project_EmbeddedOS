import sys
import dbus

if len(sys.argv) != 2:
    print("Usage: python3 usb-status.py <devpath>")
    sys.exit(1)

devpath = sys.argv[1]
bus = dbus.SystemBus()
usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
status = usb_manager.GetStatus(devpath, dbus_interface='org.example.USBManager')
print(f"Trạng thái thiết bị: {status}")