#!/bin/bash
VENDOR_ID="$1"
PRODUCT_ID="$2"

# Tìm thiết bị trong database
DEVICE_INFO=$(grep -i "^${VENDOR_ID}" /usr/local/share/usb.ids | grep -i " ${PRODUCT_ID}")

# ---- Load whitelist (vendor+product) ----
WHITELIST_FILE="/usr/local/share/usb_whitelist.txt"
if [ ! -f "$WHITELIST_FILE" ]; then
    echo "Whitelist file $WHITELIST_FILE not found!" >&2
    exit 1
fi
mapfile -t ALLOWED_DEVICES < "$WHITELIST_FILE"

function is_allowed_device() {
    local id="$1:$2"
    for allowed in "${ALLOWED_DEVICES[@]}"; do
        if [[ "$allowed" == "$id" ]]; then
            return 0
        fi
    done
    return 1
}

# ---- Kiểm tra whitelist ----
if ! is_allowed_device "$VENDOR_ID" "$PRODUCT_ID"; then
    echo "blocked"
    exit 0
fi

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