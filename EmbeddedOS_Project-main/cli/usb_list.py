import dbus

bus = dbus.SystemBus()
usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
devices = usb_manager.ListDevices(dbus_interface='org.example.USBManager')
print("Danh sách thiết bị USB:")
for dev in devices:
    print(f"- ID: {dev.get('id')}, Tên: {dev.get('product')}, Trạng thái: {dev.get('status')}")