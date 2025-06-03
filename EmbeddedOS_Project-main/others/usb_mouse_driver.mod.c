#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/export-internal.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

#ifdef CONFIG_UNWINDER_ORC
#include <asm/orc_header.h>
ORC_HEADER;
#endif

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_MITIGATION_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif



static const char ____versions[]
__used __section("__versions") =
	"\x20\x00\x00\x00\x6d\x20\x63\x07"
	"input_unregister_device\0"
	"\x10\x00\x00\x00\xba\x0c\x7a\x03"
	"kfree\0\0\0"
	"\x18\x00\x00\x00\x31\xe1\x34\x72"
	"usb_deregister\0\0"
	"\x1c\x00\x00\x00\x63\xa5\x03\x4c"
	"random_kmalloc_seed\0"
	"\x18\x00\x00\x00\x98\x04\xd2\xf2"
	"kmalloc_caches\0\0"
	"\x20\x00\x00\x00\xfe\x6e\xe0\xb2"
	"__kmalloc_cache_noprof\0\0"
	"\x20\x00\x00\x00\x05\x56\x18\x29"
	"input_allocate_device\0\0\0"
	"\x20\x00\x00\x00\xcf\xb2\xc7\xc0"
	"input_register_device\0\0\0"
	"\x1c\x00\x00\x00\xc7\xad\x2e\x24"
	"input_free_device\0\0\0"
	"\x14\x00\x00\x00\xbb\x6d\xfb\xbd"
	"__fentry__\0\0"
	"\x1c\x00\x00\x00\x3a\x81\xfa\xaf"
	"usb_register_driver\0"
	"\x1c\x00\x00\x00\xca\x39\x82\x5b"
	"__x86_return_thunk\0\0"
	"\x18\x00\x00\x00\x34\x61\x23\x68"
	"module_layout\0\0\0"
	"\x00\x00\x00\x00\x00\x00\x00\x00";

MODULE_INFO(depends, "");

MODULE_ALIAS("usb:v10C4p8105d*dc*dsc*dp*ic*isc*ip*in*");

MODULE_INFO(srcversion, "3F2A3E27A58A77F6AA4ECA7");
