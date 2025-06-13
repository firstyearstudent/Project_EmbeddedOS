# EmbeddedOS USB Management Project

## Mục lục
- [Tổng quan](#tổng-quan)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Cài đặt & Thiết lập](#cài-đặt--thiết-lập)
- [Khởi động & Chạy dự án](#khởi-động--chạy-dự-án)
- [Biên dịch Kernel Modules (Tùy chọn)](#biên-dịch-kernel-modules-tùy-chọn)
- [Chạy dịch vụ DBus](#chạy-dịch-vụ-dbus)
- [Sử dụng Giao diện Đồ họa (GUI)](#sử-dụng-giao-diện-đồ-họa-gui)
- [Sử dụng Công cụ Dòng lệnh (CLI)](#sử-dụng-công-cụ-dòng-lệnh-cli)
- [Chạy như một dịch vụ Systemd](#chạy-như-một-dịch-vụ-systemd)
- [Khắc phục sự cố](#khắc-phục-sự-cố)
- [Tác giả & Cộng tác viên](#tác-giả--cộng-tác-viên)

---

## Tổng quan
Dự án cung cấp giải pháp quản lý thiết bị USB hoàn chỉnh cho hệ thống Linux nhúng (ví dụ: Raspberry Pi 4), bao gồm:
- Kernel modules phát hiện thiết bị USB (tùy chọn)
- Dịch vụ DBus quản lý USB
- Giao diện đồ họa Python (GUI) điều khiển thiết bị USB
- Bộ công cụ CLI cho tự động hóa và script
- Hỗ trợ plugin cho các hành động tùy chỉnh theo thiết bị

---

## Yêu cầu hệ thống
- **Hệ điều hành:** Linux (đã kiểm thử trên Ubuntu, Raspberry Pi OS)
- **Python:** 3.6 trở lên
- **Gói hệ thống:**
  - `python3-gi` (PyGObject)
  - `python3-dbus` (dbus-python)
  - `udisks2`
  - `systemd` (quản lý dịch vụ)
  - `build-essential`, `linux-headers-$(uname -r)` (cho kernel modules, tùy chọn)
- **Gói Python:**
  - `pyudev`

**Cài đặt tất cả yêu cầu:**
```bash
sudo apt update
sudo apt install python3-gi python3-dbus udisks2 systemd build-essential linux-headers-$(uname -r) python3-pip
pip3 install pyudev
```

---

## Cấu trúc dự án
```
EmbeddedOS_Project-main/
├── usb_manager_gui.py         # Giao diện đồ họa Python
├── usb_ids.txt               # CSDL thiết bị USB
├── usb_management/           # Script quản lý & plugin
├── others/                   # Kernel modules (tùy chọn)
├── cli/                      # Công cụ dòng lệnh
├── systemd/                  # File dịch vụ systemd
└── README.md                 # Hướng dẫn sử dụng
```

---

## Cài đặt & Thiết lập

1. **Tải hoặc clone dự án về máy Linux của bạn.**
2. **Cài đặt tất cả các yêu cầu** như ở trên.
3. **(Tùy chọn) Chỉnh sửa file `usb_ids.txt`** để thêm thiết bị của bạn vào whitelist hoặc gắn nhãn.

---

## Khởi động & Chạy dự án

### 1. Khởi động dịch vụ DBus (bắt buộc)

Bạn cần khởi động dịch vụ DBus trước khi sử dụng GUI hoặc CLI.

**Chạy trực tiếp (testing):**
```bash
cd usb_management
sudo python3 dbus_service.py
```
- Dịch vụ sẽ chạy nền, quản lý các yêu cầu liên quan đến USB.

**Chạy bằng systemd (khuyến nghị cho môi trường production):**
1. Mở file `systemd/dbus.service` và chỉnh đường dẫn tuyệt đối đến script:
   ```
   ExecStart=/usr/bin/python3 /ABSOLUTE/PATH/TO/EmbeddedOS_Project-main/usb_management/dbus_service.py
   ```
2. Cài đặt và kích hoạt dịch vụ:
   ```bash
   sudo cp systemd/dbus.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable dbus
   sudo systemctl start dbus
   sudo systemctl status dbus
   ```

### 2. Chạy giao diện đồ họa (GUI)

**Chạy GUI:**
```bash
python3 usb_manager_gui.py
```
- Đảm bảo dịch vụ DBus đã chạy trước khi khởi động GUI.

### 3. Sử dụng các công cụ CLI

- Liệt kê thiết bị USB:
  ```bash
  python3 cli/usb_list.py
  ```
- Gắn một thiết bị:
  ```bash
  python3 cli/usb_mount.py <serial|devpath>
  ```
- Tháo thiết bị:
  ```bash
  python3 cli/usb_unmount.py <serial|devpath>
  ```
- Kiểm tra trạng thái thiết bị:
  ```bash
  python3 cli/usb_status.py <serial|devpath>
  ```

---

## Biên dịch Kernel Modules (Tùy chọn)
Nếu bạn muốn sử dụng các kernel module tự viết cho phát hiện thiết bị USB:
```bash
cd others
make clean
make
```
**Nạp module:**
```bash
sudo insmod usb_audio_driver.ko
sudo insmod usb_storage_driver.ko
sudo insmod usb_hid_driver.ko
sudo insmod usb_video_driver.ko
```
**Kiểm tra log kernel:**
```bash
dmesg | tail
```
> **Lưu ý:** Phần lớn người dùng không cần nạp các module này trừ khi muốn thử nghiệm driver tùy chỉnh.

---

## Chạy dịch vụ DBus

Xem phần [Khởi động & Chạy dự án](#khởi-động--chạy-dự-án).

---

## Sử dụng Giao diện Đồ họa (GUI)

1. Đảm bảo dịch vụ DBus đã chạy.
2. Chạy:
   ```bash
   python3 usb_manager_gui.py
   ```
3. **Tính năng:**
   - Xem tất cả thiết bị USB đang kết nối
   - Gắn/tháo thiết bị
   - Làm mới danh sách thiết bị
   - Nhận thông báo lỗi nếu DBus chưa chạy hoặc thao tác thất bại

---

## Sử dụng Công cụ Dòng lệnh (CLI)

Xem mục [Chạy & Sử dụng CLI](#khởi-động--chạy-dự-án).

---

## Chạy như một dịch vụ Systemd (usb_classifier)
Nếu bạn muốn sử dụng daemon phân loại USB:
1. Sửa file `systemd/usb_classifier.service` và chỉnh đường dẫn tuyệt đối:
   ```
   ExecStart=/usr/bin/python3 /ABSOLUTE/PATH/TO/EmbeddedOS_Project-main/usb_management/usb_classify.py
   ```
2. Copy & kích hoạt dịch vụ:
   ```bash
   sudo cp systemd/usb_classifier.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable usb_classifier
   sudo systemctl start usb_classifier
   sudo systemctl status usb_classifier
   ```

---

## Khắc phục sự cố

- **Permission denied cho log:**  
  - Chạy script với `sudo` hoặc đổi đường dẫn log sang thư mục có quyền ghi.
- **Lỗi kết nối DBus:**  
  - Đảm bảo dịch vụ DBus đang chạy.
- **Module lỗi định dạng:**  
  - Biên dịch lại kernel module với đúng kernel headers.
- **Thiết bị không xuất hiện:**  
  - Kiểm tra `usb_ids.txt` và log hệ thống (`dmesg`, `journalctl`).
- **GUI không cập nhật:**  
  - Nhấn "Refresh" hoặc khởi động lại GUI sau khi cắm/tháo thiết bị.

---

## Tác giả & Cộng tác viên
- Dự án bởi Nhóm 13
