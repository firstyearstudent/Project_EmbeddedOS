#include <stdio.h>
#include <libusb-1.0/libusb.h>

int main() {
    libusb_device **devs;
    libusb_context *ctx = NULL;
    ssize_t cnt;
    int r = libusb_init(&ctx);
    if (r < 0) return 1;

    cnt = libusb_get_device_list(ctx, &devs);
    for (ssize_t i = 0; i < cnt; i++) {
        struct libusb_device_descriptor desc;
        libusb_get_device_descriptor(devs[i], &desc);
        printf("Vendor: %04x, Product: %04x, Class: %02x\n", desc.idVendor, desc.idProduct, desc.bDeviceClass);

        switch(desc.bDeviceClass) {
            case 0x08: printf("  Loại: Mass Storage\n"); break;
            case 0x03: printf("  Loại: HID\n"); break;
            case 0x01: printf("  Loại: Audio\n"); break;
            case 0x0e: printf("  Loại: Video\n"); break;
            default:   printf("  Loại: Khác\n");
        }
    }
    libusb_free_device_list(devs, 1);
    libusb_exit(ctx);
    return 0;
}