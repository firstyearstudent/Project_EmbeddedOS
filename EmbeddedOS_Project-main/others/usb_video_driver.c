#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/usb.h>

static struct usb_device_id video_ids[] = {
    { USB_INTERFACE_INFO(USB_CLASS_VIDEO, 1, 0) },
    { }
};
MODULE_DEVICE_TABLE(usb, video_ids);

static int usb_video_probe(struct usb_interface *interface, const struct usb_device_id *id)
{
    struct usb_device *usb_dev = interface_to_usbdev(interface);

    printk(KERN_INFO "[usb_video_driver] Video Device: VID=%04x PID=%04x\n",
           le16_to_cpu(usb_dev->descriptor.idVendor),
           le16_to_cpu(usb_dev->descriptor.idProduct));

    return 0;
}

static void usb_video_disconnect(struct usb_interface *interface)
{
    printk(KERN_INFO "[usb_video_driver] Video Device disconnected\n");
}

static struct usb_driver usb_video_driver = {
    .name = "usb_video_driver",
    .id_table = video_ids,
    .probe = usb_video_probe,
    .disconnect = usb_video_disconnect,
};

module_usb_driver(usb_video_driver);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("QQP Group & Copilot");
MODULE_DESCRIPTION("USB Video Detection Driver");