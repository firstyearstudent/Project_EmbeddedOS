def can_handle(device):
    """
    Kiểm tra thiết bị có phải là thiết bị USB Audio không.
    """
    # USB Audio class code là 0x01
    usb_class = device.get('ID_USB_CLASS')
    if usb_class == '01' or usb_class == 1:
        return True
    # Một số hệ thống có thể dùng ID_USB_DRIVER
    if device.get('ID_USB_DRIVER') == 'snd-usb-audio':
        return True
    return False

def handle(device, action):
    """
    Xử lý sự kiện thiết bị audio được kết nối hoặc tháo ra.
    """
    name = device.get('ID_MODEL', 'Unknown Audio Device')
    vendor = device.get('ID_VENDOR', 'Unknown Vendor')
    devnode = device.get('DEVNAME', 'N/A')
    if action == 'add':
        print(f"[AUDIO PLUGIN] Thiết bị audio được kết nối: {name} ({vendor}) tại {devnode}")
    elif action == 'remove':
        print(f"[AUDIO PLUGIN] Thiết bị audio đã tháo: {name} ({vendor}) tại {devnode}")
    else:
        print(f"[AUDIO PLUGIN] Sự kiện không xác định: {action} cho thiết bị {name}")