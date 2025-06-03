#!/bin/bash
# File: /usr/local/bin/usb_handler.sh
# Description: Universal USB device handler with dynamic classification
# Version: 2.0
# Requires: usb.ids database (auto-downloaded), udev, logger

# ---- Cấu hình hệ thống ----
LOG_FILE="/var/log/usb_handler.log"
MOUNT_BASE="/mnt/usb"
ALLOWED_VENDORS=("0781" "090c")  # SanDisk, Silicon Motion
BLACKLISTED_CLASSES=("ff" "00")  # Vendor-specific classes

# ---- Khởi tạo ----
DEVICE_PATH="$1"
VENDOR_ID=$(udevadm info -q property -n "$DEVICE_PATH" | grep "ID_VENDOR_ID" | cut -d= -f2)
PRODUCT_ID=$(udevadm info -q property -n "$DEVICE_PATH" | grep "ID_MODEL_ID" | cut -d= -f2)
SERIAL=$(udevadm info -q property -n "$DEVICE_PATH" | grep "ID_SERIAL_SHORT" | cut -d= -f2)
CLASS_CODE=$(udevadm info -q property -n "$DEVICE_PATH" | grep "ID_USB_CLASS" | cut -d= -f2)

# ---- Hàm tiện ích ----
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    logger -t "usb_handler" "$1"
}

mount_device() {
    local dev="$1"
    local mount_point="${MOUNT_BASE}_${VENDOR_ID}_${PRODUCT_ID}_${SERIAL}"
    
    mkdir -p "$mount_point" || { log "Failed to create mount point"; return 1; }
    
    # Thử các filesystem phổ biến
    for fs in vfat ntfs ext4 exfat; do
        if mount -t "$fs" -o uid=1000,gid=1000,noexec,nodev,nosuid "$dev" "$mount_point" 2>/dev/null; then
            log "Mounted $dev ($fs) at $mount_point"
            chown $USER: "$mount_point"
            return 0
        fi
    done
    
    log "Failed to mount $dev (tried vfat, ntfs, ext4, exfat)"
    return 1
}

# ---- Kiểm tra bảo mật ----
# Chặn thiết bị không có trong whitelist
if [[ ! " ${ALLOWED_VENDORS[@]} " =~ " ${VENDOR_ID} " ]]; then
    log "Blocked unauthorized device: $VENDOR_ID:$PRODUCT_ID"
    exit 1
fi

# Chặn lớp thiết bị nguy hiểm
if [[ " ${BLACKLISTED_CLASSES[@]} " =~ " ${CLASS_CODE} " ]]; then
    log "Blocked blacklisted class: $CLASS_CODE (device $VENDOR_ID:$PRODUCT_ID)"
    exit 1
fi

# ---- Phân loại chính ----
case "$CLASS_CODE" in
    08)  # Mass Storage
        if [[ "$DEVICE_PATH" == *"sd"* ]]; then
            mount_device "/dev/${DEVICE_PATH##*/}"
        else
            log "Unsupported storage device path: $DEVICE_PATH"
        fi
        ;;
    03)  # HID
        MODULE="usbhid"
        if lsusb -d "$VENDOR_ID:$PRODUCT_ID" | grep -qi "keyboard"; then
            MODULE="usbkbd"
        fi
        modprobe "$MODULE" && log "Loaded $MODULE for $VENDOR_ID:$PRODUCT_ID"
        ;;
    01)  # Audio
        pulseaudio --start
        log "Audio device connected, restarted PulseAudio"
        ;;
    0e)  # Video
        systemctl restart v4l2.service
        log "Video device connected, restarted v4l2"
        ;;
    *)
        # Phân loại dự phòng bằng USB ID database
        USB_INFO=$(grep -i "^$VENDOR_ID" /usr/share/usb.ids | grep -i "$PRODUCT_ID")
        case "$USB_INFO" in
            *"Hub"*)
                log "USB Hub connected, no action needed"
                ;;
            *"Printer"*)
                systemctl restart cups
                log "Printer connected, restarted CUPS"
                ;;
            *)
                log "Unknown device: $VENDOR_ID:$PRODUCT_ID - Info: $USB_INFO"
                ;;
        esac
        ;;
esac

# ---- Dọn dẹp ----
if [ -f "/tmp/usb_${DEVICE_PATH##*/}.lock" ]; then
    rm -f "/tmp/usb_${DEVICE_PATH##*/}.lock"
fi

exit 0
