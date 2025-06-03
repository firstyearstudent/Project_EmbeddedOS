#!/usr/bin/python3
import pyudev
import subprocess
import logging
from datetime import datetime
from dbus_service import start_dbus_service
from plugin_loader import PluginLoader
import threading

# ---- Cấu hình hệ thống ----
LOG_FILE = "/var/log/usb_classifier.log"
MOUNT_BASE = "/mnt/usb"
WHITELIST_VENDORS = ["0781", "090c"]  # SanDisk, Silicon Motion

# ---- Thiết lập logging ----
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_event(device, classification):
    """Ghi log sự kiện USB"""
    vendor = device.get('ID_VENDOR_ID', 'unknown')
    product = device.get('ID_MODEL_ID', 'unknown')
    serial = device.get('ID_SERIAL_SHORT', 'unknown')
    
    logging.info(
        f"Device {device.device_node}: "
        f"Vendor={vendor}, Product={product}, "
        f"Serial={serial}, Class={classification}"
    )

def classify_device(device):
    """Phân loại thiết bị với thuật toán cải tiến"""
    usb_class = device.get('ID_USB_INTERFACES', '').lower()
    vendor = device.get('ID_VENDOR_ID', '')
    
    # Kiểm tra whitelist
    if vendor not in WHITELIST_VENDORS:
        return "blocked"
    
    # Phân loại theo class code
    if '08' in usb_class:
        return "storage"
    elif '03' in usb_class:
        return "hid"
    elif '01' in usb_class:
        return "audio"
    elif '0e' in usb_class:
        return "video"
    
    # Phân loại dự phòng bằng USB ID database
    try:
        output = subprocess.check_output(
            f"lsusb -d {vendor}:{product}",
            shell=True,
            text=True
        )
        if 'storage' in output.lower():
            return "storage"
        elif 'keyboard' in output.lower() or 'mouse' in output.lower():
            return "hid"
    except:
        pass
    
    return "unknown"

def handle_device(device, classification):
    """Xử lý thiết bị theo phân loại"""
    dev_node = device.device_node
    
    if classification == "blocked":
        logging.warning(f"Blocked unauthorized device: {dev_node}")
        return
        
    try:
        if classification == "storage":
            mount_point = f"{MOUNT_BASE}_{device.get('ID_VENDOR_ID')}_{device.get('ID_MODEL_ID')}"
            subprocess.run([
                "mount", 
                "-o", "uid=1000,gid=1000,noexec", 
                dev_node, 
                mount_point
            ], check=True)
            
        elif classification == "hid":
            subprocess.run([
                "modprobe", 
                "usbhid"
            ], check=True)
            
        log_event(device, classification)
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to handle {dev_node}: {str(e)}")

# ---- Main Execution ----
if __name__ == "__main__":
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('usb')
    
    logging.info("USB Classifier Daemon Started")
    
    for device in iter(monitor.poll, None):
        if device.action == 'add':
            classification = classify_device(device)
            handle_device(device, classification)

def main():
    # ... (khởi tạo context, monitor)
    
    # Khởi tạo plugin loader
    plugin_loader = PluginLoader("/path/to/plugins")
    plugin_loader.load_plugins()
    
    # Khởi chạy D-Bus service trong thread riêng
    dbus_thread = threading.Thread(target=start_dbus_service, args=(plugin_loader,))
    dbus_thread.daemon = True
    dbus_thread.start()
    
    for device in iter(monitor.poll, None):
        if device.action == 'add':
            # Gửi signal qua D-Bus
            # service.DeviceAdded(vendor, product, dev_type)
            
            # Xử lý qua plugin
            plugin_loader.handle_device(device, 'add')
            
        elif device.action == 'remove':
            plugin_loader.handle_device(device, 'remove')