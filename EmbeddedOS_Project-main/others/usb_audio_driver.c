#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/usb.h>

static struct usb_device_id audio_ids[] = {
    { USB_INTERFACE_INFO(USB_CLASS_AUDIO, 1, 0) },
    { }
};
MODULE_DEVICE_TABLE(usb, audio_ids);

static int usb_audio_probe(struct usb_interface *interface, const struct usb_device_id *id)
{
    struct usb_device *usb_dev = interface_to_usbdev(interface);

    printk(KERN_INFO "[usb_audio_driver] Audio Device: VID=%04x PID=%04x\n",
           le16_to_cpu(usb_dev->descriptor.idVendor),
           le16_to_cpu(usb_dev->descriptor.idProduct));

    return 0;
}

static void usb_audio_disconnect(struct usb_interface *interface)
{
    printk(KERN_INFO "[usb_audio_driver] Audio Device disconnected\n");
}

static struct usb_driver usb_audio_driver = {
    .name = "usb_audio_driver",
    .id_table = audio_ids,
    .probe = usb_audio_probe,
    .disconnect = usb_audio_disconnect,
};

module_usb_driver(usb_audio_driver);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("QQP Group & Copilot");
MODULE_DESCRIPTION("USB Audio Detection Driver");