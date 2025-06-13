#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/usb.h>
#include <linux/input.h>
 

static struct usb_device_id mouse_ids[] = {
    { USB_DEVICE(0x10c4, 0x8105) },  
    { }
};
MODULE_DEVICE_TABLE(usb, mouse_ids);

// Cấu trúc dữ liệu cho driver chuột
struct usb_mouse {
    struct usb_device *usb_dev;
    struct input_dev *input_dev;
};

// Hàm probe: Khởi tạo khi thiết bị USB được kết nối
static int usb_mouse_probe(struct usb_interface *interface, const struct usb_device_id *id)
{
    struct usb_mouse *mouse;
    struct usb_device *usb_dev = interface_to_usbdev(interface);
    struct input_dev *input_dev;

    mouse = kzalloc(sizeof(struct usb_mouse), GFP_KERNEL);
    if (!mouse)
        return -ENOMEM;

    input_dev = input_allocate_device();
    if (!input_dev) {
        kfree(mouse);
        return -ENOMEM;
    }

    input_dev->name = "USB Mouse";
    input_dev->phys = "usb-input";
    input_dev->id.bustype = BUS_USB;
    // Vendor và Product ID được lấy tự động từ thiết bị, không cần thay đổi ở đây
    input_dev->id.vendor = le16_to_cpu(usb_dev->descriptor.idVendor);
    input_dev->id.product = le16_to_cpu(usb_dev->descriptor.idProduct);

    // Thiết lập sự kiện cho chuột (phím và di chuyển)
    __set_bit(EV_KEY, input_dev->evbit);
    __set_bit(EV_REL, input_dev->evbit);
    __set_bit(BTN_LEFT, input_dev->keybit);
    __set_bit(BTN_RIGHT, input_dev->keybit);
    __set_bit(REL_X, input_dev->relbit);
    __set_bit(REL_Y, input_dev->relbit);

    if (input_register_device(input_dev)) {
        input_free_device(input_dev);
        kfree(mouse);
        return -ENOMEM;
    }

    mouse->input_dev = input_dev;
    mouse->usb_dev = usb_dev;
    usb_set_intfdata(interface, mouse);

    return 0;
}

// Hàm disconnect: Dọn dẹp khi thiết bị USB bị ngắt kết nối
static void usb_mouse_disconnect(struct usb_interface *interface)
{
    struct usb_mouse *mouse = usb_get_intfdata(interface);

    input_unregister_device(mouse->input_dev);
    kfree(mouse);
}

// Cấu trúc driver USB
static struct usb_driver usb_mouse_driver = {
    .name = "usb_mouse",
    .id_table = mouse_ids,
    .probe = usb_mouse_probe,
    .disconnect = usb_mouse_disconnect,
};

// Hàm khởi tạo module
static int __init usb_mouse_init(void)
{
    return usb_register(&usb_mouse_driver);
}

// Hàm thoát module
static void __exit usb_mouse_exit(void)
{
    usb_deregister(&usb_mouse_driver);
}

module_init(usb_mouse_init);
module_exit(usb_mouse_exit);

// Thông tin module
MODULE_LICENSE("GPL");
MODULE_AUTHOR("QQP Group");
MODULE_DESCRIPTION("USB Mouse Driver");
