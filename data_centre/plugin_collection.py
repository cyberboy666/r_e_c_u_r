import inspect
import os
import pkgutil


class Plugin(object):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """

    def __init__(self, plugin_collection):
        self.description = 'UNKNOWN'
        self.pc = plugin_collection

    def perform_operation(self, argument):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call
        """
        raise NotImplementedError

class MidiFeedbackPlugin(Plugin):
    """Base class for MIDI feedback plugins
    """
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)
        self.description = 'Outputs feedback about status to device eg MIDI pads'
        self.pc = plugin_collection

    def supports_midi_feedback(self, device_name):
        return False

    def set_midi_device(self, midi_device):
        self.midi_feedback_device = midi_device

    def perform_operation(self, argument):
        """The actual implementation of the identity plugin is to just return the
        argument
        """
        return argument


# adapted from https://github.com/gdiepen/python_plugin_example
class PluginCollection(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    def __init__(self, plugin_package, message_handler, data):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugin_package = plugin_package
        self.message_handler = message_handler
        self.data = data
        #self.actions = message_handler.actions
        self.reload_plugins()


    def reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.plugins = []
        self.seen_paths = []
        print()
        print("Looking for plugins under package %s" % self.plugin_package)
        self.walk_package(self.plugin_package)


    def get_plugins(self, clazz = None):
        if clazz:
            return [c for c in self.plugins if isinstance(c, clazz)]
        else:
            return self.plugins

    def apply_all_plugins_on_value(self, argument):
        """Apply all of the plugins on the argument supplied to this function
        """
        print()
        print('Applying all plugins on value %s:' %argument)
        for plugin in self.plugins:
            print(" Applying %s on value %s yields value %s" % (plugin.description, argument, plugin.perform_operation(argument)))

    def walk_package(self, package):
        """Recursively walk the supplied package to retrieve all plugins
        """
        imported_package = __import__(package, fromlist=['blah'])

        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not ispkg:
                plugin_module = __import__(pluginname, fromlist=['blah'])
                clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                    if issubclass(c, Plugin) & (c is not Plugin):
                        print('    Found plugin class: %s.%s' % (c.__module__,c.__name__))
                        self.plugins.append(c(self))


        # Now that we have looked at all the modules in the current package, start looking
        # recursively for additional modules in sub packages
        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                # Get all sub directory of the current package path directory
                child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

                # For each sub directory, apply the walk_package method recursively
                for child_pkg in child_pkgs:
                    self.walk_package(package + '.' + child_pkg)
