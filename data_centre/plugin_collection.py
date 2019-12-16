import inspect
import os
import pkgutil
import re


class Plugin(object):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """

    def __init__(self, plugin_collection):
        self.description = 'UNKNOWN'
        self.pc = plugin_collection

class MidiFeedbackPlugin(Plugin):
    """Base class for MIDI feedback plugins
    """
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)
        self.description = 'Outputs feedback about status to device eg MIDI pads'

    def supports_midi_feedback(self, device_name):
        return False

    def set_midi_device(self, midi_device):
        self.midi_feedback_device = midi_device


class SequencePlugin(Plugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    @property
    def parserlist(self):
        return [
                # ( r"run_automation",  self.run_automation ),
                # ( r"stop_automation", self.stop_automation ),
                # ( r"toggle_automation", self.toggle_automation ),
                # ( r"toggle_pause_automation", self.toggle_pause_automation ),
        ]

    @property
    def position(self):
        import time
        passed = time.time() - self.automation_start
        if self.duration>0:
            position = passed / self.duration*1000
        else:
            position = 100 / (passed/frequency)
        return position

    def toggle_automation(self):
        if not self.is_playing():
            self.run_automation()
        else:
            self.stop_automation()

    def pause_automation(self):
        self.pause_flag = not self.is_paused() and self.is_playing()

    def stop_automation(self):
        self.stop_flag = True

    def toggle_pause_automation(self):
        self.pause_flag = not self.is_paused()
        self.pause_flag = self.is_paused() and self.is_playing()
        if self.is_playing():
            print ("playing")
        else:
            print ("not playing")
        if not self.is_paused() and not self.is_playing():
            print ("not paused, not playing - starting")
            self.run_automation()

    pause_flag = True
    stop_flag = False
    automation_start = None
    duration = 2000
    frequency = 100
    def run_automation(self):
        import time
        if not self.automation_start:
            self.automation_start = time.time()
            print ("set automation_start to %s" % self.automation_start)
            self.pause_flag = False

        #print("running automation at %s!" % self.position)
        if not self.is_paused():
            self.run_sequence(self.position)
            print ("%s: automation_start is %s" % (time.time()-self.automation_start,self.automation_start))
        else:
            pass
            self.automation_start += (time.time() - self.automation_start)
            print ("%s: reset automation_start to %s" % (time.time()-self.automation_start,self.automation_start))
            #return

        if (time.time() - self.automation_start < self.duration/1000) and not self.stop_flag:
            self.pc.midi_input.root.after(self.frequency, self.run_automation)
        else:
            print("%s: stopping ! " % (time.time() - self.automation_start) )
            self.stop_flag = False
            self.automation_start = None

    def is_paused(self):
        return self.pause_flag

    def is_playing(self):
        return self.automation_start is not None


class ActionsPlugin(Plugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    @property
    def parserlist(self):
        return [
                #( r"test_plugin", self.test_plugin )
        ]

    def is_handled(self, method_name):
        for a in self.parserlist:
            if (a[0]==method_name):
                return True
            regex = a[0]
            me = a[1]
            matches = re.match(regex, method_name)
            if matches:
                return True


    def get_callback_for_method(self, method_name, argument):
        for a in self.parserlist:
            regex = a[0]
            me = a[1]
            matches = re.search(regex, method_name)

            if matches:
                found_method = me
                parsed_args = list(map(int,matches.groups()))
                if argument:
                    args = [argument] + parsed_args
                else:
                    args = parsed_args

                return (found_method, args)

    def call_parse_method_name(self, method_name, argument):
        method, arguments = self.actions.get_callback_for_method(method_name, argument)
        method(*arguments)


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
            #print(" Applying %s on value %s yields value %s" % (plugin.description, argument, plugin.perform_operation(argument)))
            pass


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
