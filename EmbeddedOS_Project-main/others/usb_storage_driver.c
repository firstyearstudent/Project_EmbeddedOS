#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/usb.h>

static struct usb_device_id storage_ids[] = {
    { USB_INTERFACE_INFO(USB_CLASS_MASS_STORAGE, 0x06, 0x50) },
    { }
};
MODULE_DEVICE_TABLE(usb, storage_ids);

static int usb_storage_probe(struct usb_interface *interface, const struct usb_device_id *id)
{
    struct usb_device *usb_dev = interface_to_usbdev(interface);

    printk(KERN_INFO "[usb_storage_driver] Storage Device: VID=%04x PID=%04x\n",
           le16_to_cpu(usb_dev->descriptor.idVendor),
           le16_to_cpu(usb_dev->descriptor.idProduct));

    return 0;
}

static void usb_storage_disconnect(struct usb_interface *interface)
{
    printk(KERN_INFO "[usb_storage_driver] Storage Device disconnected\n");
}

static struct usb_driver usb_storage_driver = {
    .name = "usb_storage_driver",
    .id_table = storage_ids,
    .probe = usb_storage_probe,
    .disconnect = usb_storage_disconnect,
};

module_usb_driver(usb_storage_driver);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("QQP Group & Copilot");
MODULE_DESCRIPTION("USB Mass Storage Detection Driver");