obj-m += usb_hid_driver.o
obj-m += usb_storage_driver.o
obj-m += usb_video_driver.o
obj-m += usb_audio_driver.o

all:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean