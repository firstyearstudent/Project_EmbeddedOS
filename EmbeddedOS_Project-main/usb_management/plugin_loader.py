import os
import importlib.util

class PluginLoader:
    def __init__(self, plugins_dir):
        self.plugins_dir = plugins_dir
        self.plugins = []

    def load_plugins(self):
        for filename in os.listdir(self.plugins_dir):
            if filename.endswith('_plugin.py'):
                plugin_path = os.path.join(self.plugins_dir, filename)
                spec = importlib.util.spec_from_file_location(filename[:-3], plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.plugins.append(module)

    def handle_device(self, device, action):
        for plugin in self.plugins:
            if hasattr(plugin, 'can_handle') and plugin.can_handle(device):
                # Nếu plugin có hàm handle, gọi nó, nếu không chỉ trả về tên plugin
                if hasattr(plugin, 'handle'):
                    return plugin.handle(device, action)
                else:
                    return f"Handled by {plugin.__name__}"
        return None
