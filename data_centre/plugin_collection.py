import inspect
import os
import pkgutil
import re

from plugins.frame_manager import FrameManager, Frame

class Plugin(object):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """
    disabled = False

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

    def refresh_midi_feedback(self):
        raise NotImplementedError



class SequencePlugin(Plugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    @property
    def parserlist(self):
        return [
                ( r"^run_automation$",  self.run_automation ),
                ( r"^stop_automation$", self.stop_automation ),
                ( r"^toggle_pause_automation$", self.toggle_pause_automation ),
                ( r"^pause_automation$", self.pause_automation ),
                ( r"^toggle_loop_automation$", self.toggle_loop_automation ),
                ( r"^set_automation_speed$", self.set_speed ),
        ]

    def set_speed(self, speed):
        self.speed = 2.0 * (2.0*(speed-0.5))
        print ("automation speed is now %s" % self.speed)

    """def position(self, now):
        import time
        passed = now - self.automation_start
        if self.duration>0:
            position = passed / self.duration*1000
        return position"""
    position = 0.0

    def toggle_automation(self):
        if not self.is_playing():
            self.run_automation()
        else:
            self.stop_automation()

    def toggle_loop_automation(self):
        self.looping = not self.looping

    def pause_automation(self):
        self.pause_flag = not self.is_paused() and self.is_playing()

    def stop_automation(self):
        self.stop_flag = True

    def toggle_pause_automation(self):
        self.pause_flag = not self.is_paused()
        self.last_delta = -1
        #self.pause_flag = self.is_paused() and self.is_playing()
        if not self.is_paused() and self.is_playing(): #not self.is_playing():
            self.run_automation()

    last_delta = -1 
    def delta(self, now):
        if self.last_delta==-1: 
            self.last_delta = now
        r = now - self.last_delta
        self.last_delta = now
        return r

    speed = 0.25 #1.0
    def move_delta(self, delta, speed):
        self.position += delta * speed
        if self.looping and self.position>1.0:
            self.position = 0.0
        elif self.looping and self.position<0:
            self.position = 1.0

    store_passed = None
    pause_flag = True
    stop_flag = False
    looping = True
    automation_start = None
    iterations_count = 0
    duration = 2000
    frequency = 100
    def run_automation(self):
        import time

        now = time.time()

        """if self.looping and self.automation_start is not None and (now - self.automation_start >= self.duration/1000):
            print("restarting as start reached %s" % self.automation_start)
            self.iterations_count += 1
            self.automation_start = None"""

        """if not self.automation_start:
            self.automation_start = now
            print ("%s: starting automation" % self.automation_start)
            self.pause_flag = False"""

        #print("running automation at %s!" % self.position)
        if not self.is_paused():
            self.store_passed = None
            delta = self.delta(now)
            self.move_delta(delta, self.speed)
            self.run_sequence(self.position)
            #print("position is now %s" % self.position)
            #self.run_sequence(self.position(now))
            #print ("%s: automation_start is %s" % (time.time()-self.automation_start,self.automation_start))
        """else:
            #print ("%s: about to reset automation_start" % self.automation_start)
            #print ("    got passed %s" % (time.time() - self.automation_start))
            if not self.store_passed:
                self.store_passed = (now - self.automation_start)
            self.automation_start = now - self.store_passed
            #print ("%s: reset automation_start to %s" % (time.time()-self.automation_start,self.automation_start))
            #return"""

        if not self.stop_flag: # and (now - self.automation_start < self.duration/1000):
            self.pc.midi_input.root.after(self.frequency, self.run_automation)
        else:
            print("%s: stopping ! (stop_flag %s)" % ((now - self.automation_start),self.stop_flag) )
            self.stop_flag = False
            self.automation_start = None
            self.iterations_count = 0

    def is_paused(self):
        return self.pause_flag

    def is_playing(self):
        return not self.is_paused() or self.stop_flag
        #return self.automation_start is not None 

    def run_sequence(self, position):
        raise NotImplementedError

from typing import Pattern
class ActionsPlugin(Plugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    @property
    def parserlist(self):
        return [
                #( r"test_plugin", self.test_plugin )
        ]

    def is_handled(self, method_name):

        if isinstance(self, DisplayPlugin):
            if method_name in self.get_display_modes():
                return True

        for a in self.parserlist:
            if (a[0]==method_name):
                return True
            regex = a[0]
            me = a[1]
            #if not isinstance(regex, Pattern):
            #    continue

            matches = re.match(regex, method_name)

            if matches:
                return True


    def get_callback_for_method(self, method_name, argument):
        for a in self.parserlist:
            regex = a[0]
            me = a[1]
            #if not isinstance(regex, Pattern):
            #    continue

            matches = re.search(regex, method_name)

            if matches:
                found_method = me
                parsed_args = self.pc.actions.detect_types(matches.groups())
                if argument is not None:
                    args = parsed_args + [argument]
                else:
                    args = parsed_args

                return (found_method, args)

class DisplayPlugin(Plugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    def is_handled(self, name):
            raise NotImplementedError

    def get_display_modes(self):
            raise NotImplementedError

    def show_plugin(self, display):
        from tkinter import Text, END
        #display_text.insert(END, 'test from DisplayPlugin')
        display.display_text.insert(END, '{} \n'.format(display.body_title))

class ModulationReceiverPlugin(Plugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    def set_modulation_value(self, param, value):
        print("||||||set_modulation_value dummy!")
        raise NotImplementedError


# adapted from https://github.com/gdiepen/python_plugin_example
class PluginCollection(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    @property
    def shaders(self):
        return self.actions.shaders

    @property
    def actions(self):
        return self.message_handler.actions

    @property
    def midi_input(self):
        return self.data.midi_input

    def __init__(self, plugin_package, message_handler, data):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugin_package = plugin_package
        self.message_handler = message_handler
        #self.shaders = lambda: data.shaders
        self.data = data
        #self.actions = message_handler.actions
        self.reload_plugins()

        self.fm = FrameManager(self)

    def read_json(self, file_name):
        return self.data._read_plugin_json(file_name)
    def update_json(self, file_name, data):
        return self.data._update_plugin_json(file_name, data)

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
            return [c for c in self.plugins if (isinstance(c, clazz) and not c.disabled)]
        else:
            return [c for c in self.plugins if not c.disabled]

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
                    # or one of the base classes
                    ignore_list = [ Plugin, ActionsPlugin, SequencePlugin, MidiFeedbackPlugin, DisplayPlugin, ModulationReceiverPlugin ] 
                    if issubclass(c, Plugin) & (c not in ignore_list):
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
