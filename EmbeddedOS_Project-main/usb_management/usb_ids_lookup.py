import os

def load_usb_ids(usb_ids_path):
    vendors = {}
    products = {}
    current_vendor = None
    with open(usb_ids_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            if not line.startswith('\t'):
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    vendor_id, vendor_name = parts
                    current_vendor = vendor_id.lower()
                    vendors[current_vendor] = vendor_name
            else:
                parts = line.strip().split(None, 1)
                if len(parts) == 2 and current_vendor:
                    product_id, product_name = parts
                    products[(current_vendor, product_id.lower())] = product_name
    return vendors, products

def lookup_usb_name(vendor_id, product_id, usb_ids_path):
    vendors, products = load_usb_ids(usb_ids_path)
    vendor_name = vendors.get(vendor_id.lower(), vendor_id)
    product_name = products.get((vendor_id.lower(), product_id.lower()), product_id)
    return vendor_name, product_name