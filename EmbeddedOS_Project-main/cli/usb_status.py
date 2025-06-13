#!/usr/bin/env python3
import sys
import pyudev

if len(sys.argv) < 2:
    print("Usage: usb_status.py <serial|devpath>")
    sys.exit(1)

serial = sys.argv[1]
context = pyudev.Context()
found = False

for device in context.list_devices(subsystem='usb'):
    if device.get('ID_SERIAL_SHORT') == serial or device.get('DEVPATH') == serial:
        found = True
        dev_node = device.get('DEVNAME')
        if dev_node:
            # Thiết bị storage, kiểm tra mounted/unmounted
            with open('/proc/mounts', 'r') as f:
                for line in f:
                    if dev_node in line:
                        print(f"{dev_node} is mounted")
                        sys.exit(0)
            print(f"{dev_node} is not mounted")
            sys.exit(0)
        else:
            # Thiết bị USB không phải storage
            print("Device is connected (not a storage device)")
            sys.exit(0)

if not found:
    print("Device not found")
    sys.exit(1)