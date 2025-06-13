#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/usb.h>
#include <linux/input.h>
#include <linux/slab.h>

#define USB_INTERFACE_CLASS_HID 0x03
static struct usb_device_id hid_ids[] = {
    { USB_INTERFACE_INFO(USB_INTERFACE_CLASS_HID, 0, 0) },
    { }
};
MODULE_DEVICE_TABLE(usb, hid_ids);

struct usb_hid_dev {
    struct usb_device *usb_dev;
    struct input_dev *input_dev;
};

static int usb_hid_probe(struct usb_interface *interface, const struct usb_device_id *id)
{
    struct usb_hid_dev *hid;
    struct usb_device *usb_dev = interface_to_usbdev(interface);
    struct input_dev *input_dev;

    hid = kzalloc(sizeof(struct usb_hid_dev), GFP_KERNEL);
    if (!hid)
        return -ENOMEM;

    input_dev = input_allocate_device();
    if (!input_dev) {
        kfree(hid);
        return -ENOMEM;
    }

    input_dev->name = "USB HID Device";
    input_dev->phys = "usb-hid-input";
    input_dev->id.bustype = BUS_USB;
    input_dev->id.vendor = le16_to_cpu(usb_dev->descriptor.idVendor);
    input_dev->id.product = le16_to_cpu(usb_dev->descriptor.idProduct);

    __set_bit(EV_KEY, input_dev->evbit);
    __set_bit(EV_REL, input_dev->evbit);
    __set_bit(KEY_A, input_dev->keybit);
    __set_bit(KEY_B, input_dev->keybit);

    if (input_register_device(input_dev)) {
        input_free_device(input_dev);
        kfree(hid);
        return -ENOMEM;
    }

    hid->input_dev = input_dev;
    hid->usb_dev = usb_dev;
    usb_set_intfdata(interface, hid);

    printk(KERN_INFO "[usb_hid_driver] HID Device connected: VID=%04x PID=%04x\n",
           input_dev->id.vendor, input_dev->id.product);

    return 0;
}

static void usb_hid_disconnect(struct usb_interface *interface)
{
    struct usb_hid_dev *hid = usb_get_intfdata(interface);

    input_unregister_device(hid->input_dev);
    kfree(hid);

    printk(KERN_INFO "[usb_hid_driver] HID Device disconnected\n");
}

static struct usb_driver usb_hid_driver = {
    .name = "usb_hid_driver",
    .id_table = hid_ids,
    .probe = usb_hid_probe,
    .disconnect = usb_hid_disconnect,
};

module_usb_driver(usb_hid_driver);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("QQP Group & Copilot");
MODULE_DESCRIPTION("USB HID Detection Driver");