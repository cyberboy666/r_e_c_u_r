import inspect
import os
import pkgutil
import re

from plugins.frame_manager import FrameManager, Frame

class Plugin(object):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """
    @property
    def disabled(self):
        return type(self).__name__ not in self.pc.data.get_enabled_plugin_class_names()

    def __init__(self, plugin_collection):
        self.description = 'UNKNOWN'
        self.pc = plugin_collection

    def stop_plugin(self):
        print(">>Stopping plugin " + type(self).__name__)

    def start_plugin(self):
        print(">>Starting plugin " + type(self).__name__)

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
    """Base class for plugins that run constantly or on demand for eg automation"""
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
        #self.speed = 2.0 * (2.0*(speed-0.5))
        speed = 2.0*(speed-0.5) # adjust to range -1 to +1
        negative = speed<0.0 # remember negative state cos we'll lose it in next
        self.speed = (speed * speed) * 2.0
        if negative: self.speed *= -1
        print ("automation speed is now %s" % self.speed)

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
        if self.position>1.0:
            self.position = self.position-1.0
            self.iterations_count += 1
        elif self.position<0.0:
            self.position = self.position+1.0
            self.iterations_count += 1

    position = 0.0
    store_passed = None
    pause_flag = True
    stop_flag = False
    looping = True
    iterations_count = 0
    duration = 2000
    frequency = 100
    def run_automation(self):
        import time

        now = time.time()

        #print("running automation at %s!" % self.position)
        if not self.is_paused():
            self.store_passed = None
            delta = self.delta(now)
            self.move_delta(delta, self.speed)
            self.run_sequence(self.position)

        if not self.stop_flag and not self.disabled:
            self.pc.midi_input.root.after(self.frequency, self.run_automation)
        else:
            #print("%s: stopping ! (stop_flag %s)" % ((now - self.automation_start),self.stop_flag) )
            self.stop_flag = False
            #self.automation_start = None
            self.iterations_count = 0

    def is_paused(self):
        return self.pause_flag

    def is_playing(self):
        return not self.is_paused() or self.stop_flag
        #return self.automation_start is not None 

    def run_sequence(self, position):
        raise NotImplementedError

class ActionsPlugin(Plugin):
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    @property
    def parserlist(self):
        return [
                #( r"^test_plugin$", self.test_plugin )
        ]

    # test if this plugin should handle the method name -- also covers if we're a DisplayPlugin
    def is_handled(self, method_name):
        if isinstance(self, DisplayPlugin):
            if method_name in self.get_display_modes():
                return True

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
                parsed_args = self.pc.actions.detect_types(matches.groups())
                if argument is not None:
                    args = parsed_args + [argument]
                else:
                    args = parsed_args

                return (found_method, args)

class DisplayPlugin(Plugin):
    """Base class for plugins that want to show a user interface on the recur screen"""
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
    """Base class for plugins that want to be notified of a change to modulation values"""
    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    def set_modulation_value(self, param, value):
        print("||||||set_modulation_value dummy!")
        raise NotImplementedError

class AutomationSourcePlugin(Plugin):
    """Base class for plugins that offer things to save&playback to&from automation"""
    @property
    def frame_key(self):
        return self.__class__.__name__

    def __init__(self, plugin_collection):
        super().__init__(plugin_collection)

    def get_frame_data(self):
        raise NotImplementedError

    def recall_frame_data(self, data):
        raise NotImplementedError

    # these frame stubs deal with the simplest case of a frame being a dict of values
    # if its anything more complicated than that (like lists) then that will need to be
    # handled in the plugin by overriding these methods
    def get_frame_diff(self, last_frame, current_frame):
        lf = last_frame.get(self.frame_key)
        cf = current_frame.get(self.frame_key)

        if cf is None or not cf:
            return {}

        if lf is None or not lf:
            return cf.copy()

        diff = {}
        for queue,message in cf.items():
            if lf.get(queue) is None or lf.get(queue)!=message:
                diff[queue] = message

        #print (">>>>>> returning diff\n%s\n<<<<<" % diff)
        return diff

    def merge_data(self, data1, data2):
        #print (">>>merge_data passed\n\t%s\nand\n\t%s" % (data1,data2))
        output = {}
        if data1 is None:
            output = data2.copy()
        else:
            output = data1.copy()
            output.update(data2)
        #print("merge_data returning\n\t%s" % output)
        #print("<<<<<<")
        return output

    def get_ignored_data(self, data, ignored):
        #frame = self.f
        f = data.copy() #frame.get(self.frame_key,{})
        for queue,item in f.items(): #frame.get(self.frame_key,{}).items():
            if ignored.get(queue) is not None:
                #print ("\tfound that should ignore %s (%s) ?" % (queue, item))
                f[queue] = None
        return f

    def is_frame_data_empty(self, data):
        if len(data)>0:
            return False
        return True

    """def process_interpoloate_clip(self, frames):
        raise NotImplementedError"""

    ### TODO: experimental value interpolation -- doesn't work, and is slow!
    cmd_size = {}
    def process_interpolate_clip(self, frames):
        # loop over every frame
        #   for each property of each frame
        #       if its empty,
        #           find distance to next value
        #           interpolate from the last to the next value
        #       else,
        #           store as last value

        print("WJSEND got pre-interpolated clip: %s" % [ f.f for f in frames if f is not None])

        #last = [ [None]*4, [None]*4, [None]*4 ]
        last = {}

        """for findex,frame in enumerate(frames):
            if frame is None:
                continue"""

        reproc_to = 0
        queues = []# queue for queue in list(frame.f.get(self.frame_key,{}).keys()) for frame in frames ] # get all queues in all frames in clip
        for frame in frames:
            if frame is not None:
                for queue,command in frame.f.get(self.frame_key,{}).items():
                    queues.append(queue)
                    if command is not None and len(command)==2:
                        self.cmd_size[queue] = len(command[1])
                    if command is not None and command[1] is not None:
                        last[queue] = command
        queues = list(set(queues))
        print ("got queues %s" % queues)

        """distance_cache = [{}]*len(frames) # list [ dict { queue: list [ distance to next arg args ] } ]
        bob = {}
        for i in range(len(frames),0,-1):
            frame = frames[i-1]
            f = frame.f
            data = f.get(self.frame_key,None)
            if data is None:
                distance_cache[i-1] = bob"""

        def process(self, findex, frame):
            #for queue,command in enumerate(frame.f.get(self.frame_key,[])):
            data = frame.f.get(self.frame_key,None)
            #if data is None:
            #    return
            for queue in queues:
                if last.get(queue) is not None:
                  """if data.get(queue) is not None:
                    last[queue] = data.get(queue)
                    continue"""
                  for argindex,value in enumerate(last.get(queue)[1]):
                    #print ("findex %s: for argindex %s got last value %s" % (findex, argindex, value))
                    #if data is not None: print ("data queue is %s" % data.get(queue,None))
                    if data is not None and data.get(queue,None) is not None and len(data.get(queue))>0 and len(data.get(queue)[1])>argindex and data.get(queue)[1][argindex] is not None:
                        last[queue][1][argindex] = data.get(queue)[1][argindex]
                        continue
                    gap,future_value = self.get_distance_value_command(frames,findex,queue,argindex)
                    if gap==0 or future_value==value:
                        continue
                    #print("\tpassing %s and %s to interpolate" % (last[queue][argindex], future_value))
                    newvalue = self.pc.fm.interpolate(last[queue][1][argindex], future_value, gap)
                    if data is None:
                        frame.f[self.frame_key] = {}
                        data = frame.f[self.frame_key]
                    if data.get(queue) is None:
                        data[queue] = [last[queue][0], last[queue][1]]# [None]*self.cmd_size[queue]]
                    #while len(data.get(queue)[1])<argindex:
                    #    data.get(queue)[1] += [] #.append(None)
                    data.get(queue)[1][argindex] = int(newvalue)
                    last[queue][1][argindex] = int(newvalue)
                elif data is not None and data.get(queue) is not None:
                    #print("no last[%s] already set, setting to %s" % (queue, data.get(queue)))
                    last[queue] = data.get(queue)

        for i in range(1):
          for findex,frame in enumerate(frames):
            if frame is None:
                continue

            process(self,findex,frame)

        print("\nWJSEND got interpolated clip: %s" % [ f.f for f in frames if f is not None ])

        self.distance_cache = {}

    distance_cache = {}
    def get_distance_value_command(self, frames, findex, queue, argindex):

        distance_cache = self.distance_cache

        # check if we have a cached value that is lower than the findex
        if distance_cache.get(queue) is not None and len(distance_cache.get(queue))>=(argindex+1) and distance_cache.get(queue)[argindex] is not None and distance_cache.get(queue)[argindex]['position'] >= findex:
            position = distance_cache.get(queue)[argindex]['position']
            #return len(frames)-
            return abs(position-findex), distance_cache.get(queue)[argindex]['value']

        #print("\t\tget_distance_value_command(findex %s, queue %s, argindex %s)" %(findex,queue,argindex))
        for i in range(1,len(frames)):
            search_findex = i + findex
            search_findex %= len(frames)
            if frames[search_findex] is None:
                continue
            #print("\t\t\tgetting frame index %s" % search_findex)
            frame = frames[search_findex]
            data = frame.f.get(self.frame_key,None)
            #print("\t\t\tgot frame data %s" % data)
            if data is None:
                continue
            command = data.get(queue,None)
            if command is None:
                continue
            print("\t\t\tget_distance_value_command testing %s argindex %s - command looks like %s" % (queue, argindex, command))
            if len(command[1])>argindex:
                if command[1][argindex] is not None and findex!=i:
                    print("\t\t\t\t\tgot distance %s to value for argindex %s: %s" % (i, argindex, command[1][argindex]))
                    if distance_cache.get(queue) is None:
                        distance_cache[queue] = [None]*(self.cmd_size[queue])
                    #while len(distance_cache[queue])<(argindex+1):
                    #    distance_cache[queue] += [None]
                    distance_cache[queue][argindex] = { 'position': i, 'value': command[1][argindex] }
                    return i, command[1][argindex]


            """if frames[search_findex] is not None and frames[search_findex].f.get(self.frame_key,{}).get(queue,[])[argindex] is not None:
                return i, frames[search_findex].f.get(self.frame_key,{}).get(queue,[])[argindex]"""
        return 0, None


### end plugin base classes

# adapted from https://github.com/gdiepen/python_plugin_example
class PluginCollection(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """
    @property
    def display(self):
        return self.actions.display

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

        # set up a FrameManager too so that plugins can use it
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

    def quit_plugins(self):
        # tell each plugin to quit
        for plugin in self.get_plugins():
            if not plugin.disabled: plugin.stop_plugin()

    def stop_plugin_name(self, name):
        for plugin in self.get_plugins(include_disabled=True):
            if type(plugin).__name__ == name:
                plugin.stop_plugin()

    def start_plugin_name(self, name):
        #print("start_plugin_name got %s"%name)
        for plugin in self.get_plugins(include_disabled=True):
            #print("looking for %s vs %s" % (type(plugin).__name__, name))
            if type(plugin).__name__ == name:
                #print("starting %s" %name)
                plugin.start_plugin()


    def get_plugins(self, clazz = None, include_disabled = False):
        if clazz:
            return [c for c in self.plugins if isinstance(c, clazz) and (include_disabled or not c.disabled)]
        else:
            return [c for c in self.plugins if include_disabled or not c.disabled]

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
                    # or one of the base classes defined in this file
                    ignore_list = [ Plugin, ActionsPlugin, SequencePlugin, MidiFeedbackPlugin, DisplayPlugin, ModulationReceiverPlugin, AutomationSourcePlugin ] 
                    if issubclass(c, Plugin) & (c not in ignore_list):
                        print('    Found plugin class: %s.%s' % (c.__module__,c.__name__))
                        self.plugins.append(c(self))


        # Now that we have looked at all the modules in the current package, start looking
        # recursively for additional modules in sub packages
        # disabled 03-2020 to try and avoid problem with subclasses-of-subclasses being listed twice.. 
        # no adverse effects yet but may need to rethink this if plugins start getting their own subdirectories
        """all_current_paths = []
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
                    self.walk_package(package + '.' + child_pkg)"""
