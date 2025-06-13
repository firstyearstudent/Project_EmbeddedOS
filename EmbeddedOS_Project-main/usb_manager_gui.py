import tkinter as tk
from tkinter import ttk, messagebox
import dbus

def get_devices():
    try:
        bus = dbus.SystemBus()
        usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
        return [dict(dev) for dev in usb_manager.ListDevices(dbus_interface='org.example.USBManager')]
    except Exception as e:
        messagebox.showerror("Lỗi DBus", f"Không thể kết nối DBus: {e}\nHãy chắc chắn service đang chạy!")
        return []

def refresh_table(tree):
    for row in tree.get_children():
        tree.delete(row)
    devices = get_devices()
    if not devices:
        return
    for dev in devices:
        tree.insert('', 'end', values=(
            dev.get('vendor', ''),
            dev.get('product', ''),
            dev.get('vendor_id', ''),
            dev.get('product_id', ''),
            dev.get('status', ''),
            dev.get('serial', ''),
            dev.get('devname', '')
        ))

def mount_selected(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("Thông báo", "Chọn thiết bị để mount")
        return
    devname = tree.item(selected[0])['values'][6]  # cột thứ 7 là devname
    status = tree.item(selected[0])['values'][4]   # cột thứ 5 là status
    if not devname:
        messagebox.showerror("Lỗi", "Chỉ thiết bị lưu trữ mới mount được!")
        return
    if status == "mounted":
        messagebox.showinfo("Thông báo", "Thiết bị đã được mount.")
        return
    try:
        bus = dbus.SystemBus()
        usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
        result = usb_manager.MountDevice(devname, dbus_interface='org.example.USBManager')
        messagebox.showinfo("Kết quả", "Mount thành công!" if result else "Mount thất bại!")
    except Exception as e:
        messagebox.showerror("Lỗi DBus", f"Không thể mount: {e}")
    refresh_table(tree)

def unmount_selected(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("Thông báo", "Chọn thiết bị để unmount")
        return
    devname = tree.item(selected[0])['values'][6]
    status = tree.item(selected[0])['values'][4]
    if not devname:
        messagebox.showerror("Lỗi", "Chỉ thiết bị lưu trữ mới unmount được!")
        return
    if status == "unmounted":
        messagebox.showinfo("Thông báo", "Thiết bị đã unmount.")
        return
    try:
        bus = dbus.SystemBus()
        usb_manager = bus.get_object('org.example.USBManager', '/org/example/USBManager')
        result = usb_manager.UnmountDevice(devname, dbus_interface='org.example.USBManager')
        messagebox.showinfo("Kết quả", "Unmount thành công!" if result else "Unmount thất bại!")
    except Exception as e:
        messagebox.showerror("Lỗi DBus", f"Không thể unmount: {e}")
    refresh_table(tree)

root = tk.Tk()
root.title("USB Manager GUI")

tree = ttk.Treeview(root, columns=('Vendor', 'Product', 'Vendor ID', 'Product ID', 'Status', 'Serial', 'devname'), show='headings')
for col in ('Vendor', 'Product', 'Vendor ID', 'Product ID', 'Status', 'Serial', 'devname'):
    tree.heading(col, text=col)
tree.pack(fill='both', expand=True)

btn_frame = tk.Frame(root)
btn_frame.pack(fill='x')
tk.Button(btn_frame, text="Refresh", command=lambda: refresh_table(tree)).pack(side='left')
tk.Button(btn_frame, text="Mount", command=lambda: mount_selected(tree)).pack(side='left')
tk.Button(btn_frame, text="Unmount", command=lambda: unmount_selected(tree)).pack(side='left')

refresh_table(tree)
root.mainloop()