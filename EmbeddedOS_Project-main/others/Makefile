obj-m += usb_hid_driver.o
obj-m += usb_storage_driver.o
obj-m += usb_video_driver.o
obj-m += usb_audio_driver.o
KDIR := /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)
all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules				

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean
		