#!/bin/bash
VENDOR_ID="$1"
PRODUCT_ID="$2"

# Tìm thiết bị trong database
DEVICE_INFO=$(grep -i "^${VENDOR_ID}" /usr/local/share/usb.ids | grep -i " ${PRODUCT_ID}")

if [[ $DEVICE_INFO == *"Keyboard"* ]]; then
    echo "hid_keyboard"
elif [[ $DEVICE_INFO == *"Mouse"* ]]; then
    echo "hid_mouse" 
elif [[ $DEVICE_INFO == *"Storage"* ]]; then
    echo "storage"
elif [[ $DEVICE_INFO == *"Audio"* ]]; then
    echo "audio"
else
    # Phân loại dựa trên USB class code nếu không có trong database
    CLASS_CODE=$(udevadm info -q property -n /dev/bus/usb/*/${VENDOR_ID}_${PRODUCT_ID} | grep "ID_USB_CLASS=" | cut -d= -f2)
    case $CLASS_CODE in
        08) echo "storage";;
        03) echo "hid";;
        01) echo "audio";;
        *) echo "unknown";;
    esac
fi