# USB-Devices-Manager-for-Pi-4-Model-B

## USB IDs Integration

This project now supports automatic lookup of USB vendor and product names using the `usb_ids.txt` file in the project root. The Python USB classifier will use this file to provide human-readable device names in logs and for improved device classification. If the file is missing, the system will fall back to using only the raw IDs.

- To update the USB IDs database, replace `usb_ids.txt` with a newer version from [linux-usb.org](http://www.linux-usb.org/usb-ids.html).
- No additional configuration is required; the integration is automatic.